import asyncio
import concurrent.futures
import time
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
)

from langgraph.constants import (
    CONF,
    CONFIG_KEY_SEND,
    ERROR,
    INTERRUPT,
    NO_WRITES,
    PUSH,
    TAG_HIDDEN,
)
from langgraph.errors import GraphDelegate, GraphInterrupt
from langgraph.pregel.executor import Submit
from langgraph.pregel.retry import arun_with_retry, run_with_retry
from langgraph.types import PregelExecutableTask, RetryPolicy


class PregelRunner:
    """Responsible for executing a set of Pregel tasks concurrently, committing
    their writes, yielding control to caller when there is output to emit, and
    interrupting other tasks if appropriate."""

    def __init__(
        self,
        *,
        submit: Submit,
        put_writes: Callable[[str, Sequence[tuple[str, Any]]], None],
        schedule_task: Callable[
            [PregelExecutableTask, int], Optional[PregelExecutableTask]
        ],
        use_astream: bool = False,
        node_finished: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.submit = submit
        self.put_writes = put_writes
        self.use_astream = use_astream
        self.node_finished = node_finished
        self.schedule_task = schedule_task

    def tick(
        self,
        tasks: Iterable[PregelExecutableTask],
        *,
        reraise: bool = True,
        timeout: Optional[float] = None,
        retry_policy: Optional[RetryPolicy] = None,
        get_waiter: Optional[Callable[[], concurrent.futures.Future[None]]] = None,
    ) -> Iterator[None]:
        def writer(
            task: PregelExecutableTask, writes: Sequence[tuple[str, Any]]
        ) -> None:
            prev_length = len(task.writes)
            # delegate to the underlying writer
            task.config[CONF][CONFIG_KEY_SEND](writes)
            for idx, w in enumerate(task.writes):
                # find the index for the newly inserted writes
                if idx < prev_length:
                    continue
                assert writes[idx - prev_length] is w
                # bail if not a PUSH write
                if w[0] != PUSH:
                    continue
                # schedule the next task, if the callback returns one
                if next_task := self.schedule_task(task, idx):
                    # if the parent task was retried,
                    # the next task might already be running
                    if any(
                        t == next_task.id for t in futures.values() if t is not None
                    ):
                        continue
                    # schedule the next task
                    futures[
                        self.submit(
                            run_with_retry,
                            next_task,
                            retry_policy,
                            writer=writer,
                            __reraise_on_exit__=reraise,
                        )
                    ] = next_task

        tasks = tuple(tasks)
        futures: dict[concurrent.futures.Future, Optional[PregelExecutableTask]] = {}
        # give control back to the caller
        yield
        # fast path if single task with no timeout and no waiter
        if len(tasks) == 1 and timeout is None and get_waiter is None:
            t = tasks[0]
            try:
                run_with_retry(t, retry_policy, writer=writer)
                self.commit(t, None)
            except Exception as exc:
                self.commit(t, exc)
                if reraise:
                    raise
            if not futures:  # maybe `t` schuduled another task
                return
        # add waiter task if requested
        if get_waiter is not None:
            futures[get_waiter()] = None
        # execute tasks, and wait for one to fail or all to finish.
        # each task is independent from all other concurrent tasks
        # yield updates/debug output as each task finishes
        for t in tasks:
            if not t.writes:
                futures[
                    self.submit(
                        run_with_retry,
                        t,
                        retry_policy,
                        writer=writer,
                        __reraise_on_exit__=reraise,
                    )
                ] = t
        done_futures: set[concurrent.futures.Future] = set()
        end_time = timeout + time.monotonic() if timeout else None
        while len(futures) > (1 if get_waiter is not None else 0):
            done, inflight = concurrent.futures.wait(
                futures,
                return_when=concurrent.futures.FIRST_COMPLETED,
                timeout=(max(0, end_time - time.monotonic()) if end_time else None),
            )
            if not done:
                break  # timed out
            for fut in done:
                task = futures.pop(fut)
                if task is None:
                    # waiter task finished, schedule another
                    if inflight and get_waiter is not None:
                        futures[get_waiter()] = None
                else:
                    # store for panic check
                    done_futures.add(fut)
                    # task finished, commit writes
                    self.commit(task, _exception(fut))
            else:
                # remove references to loop vars
                del fut, task
            # maybe stop other tasks
            if _should_stop_others(done):
                break
            # give control back to the caller
            yield
        # panic on failure or timeout
        _panic_or_proceed(
            done_futures.union(f for f, t in futures.items() if t is not None),
            panic=reraise,
        )

    async def atick(
        self,
        tasks: Iterable[PregelExecutableTask],
        *,
        reraise: bool = True,
        timeout: Optional[float] = None,
        retry_policy: Optional[RetryPolicy] = None,
        get_waiter: Optional[Callable[[], asyncio.Future[None]]] = None,
    ) -> AsyncIterator[None]:
        def writer(
            task: PregelExecutableTask, writes: Sequence[tuple[str, Any]]
        ) -> None:
            prev_length = len(task.writes)
            # delegate to the underlying writer
            task.config[CONF][CONFIG_KEY_SEND](writes)
            for idx, w in enumerate(task.writes):
                # find the index for the newly inserted writes
                if idx < prev_length:
                    continue
                assert writes[idx - prev_length] is w
                # bail if not a PUSH write
                if w[0] != PUSH:
                    continue
                # schedule the next task, if the callback returns one
                if next_task := self.schedule_task(task, idx):
                    # if the parent task was retried,
                    # the next task might already be running
                    if any(
                        t == next_task.id for t in futures.values() if t is not None
                    ):
                        continue
                    # schedule the next task
                    futures[
                        cast(
                            asyncio.Future,
                            self.submit(
                                arun_with_retry,
                                next_task,
                                retry_policy,
                                stream=self.use_astream,
                                writer=writer,
                                __name__=t.name,
                                __cancel_on_exit__=True,
                                __reraise_on_exit__=reraise,
                            ),
                        )
                    ] = next_task

        loop = asyncio.get_event_loop()
        tasks = tuple(tasks)
        futures: dict[asyncio.Future, Optional[PregelExecutableTask]] = {}
        # give control back to the caller
        yield
        # fast path if single task with no waiter and no timeout
        if len(tasks) == 1 and get_waiter is None and timeout is None:
            t = tasks[0]
            try:
                await arun_with_retry(
                    t, retry_policy, stream=self.use_astream, writer=writer
                )
                self.commit(t, None)
            except Exception as exc:
                self.commit(t, exc)
                if reraise:
                    raise
            if not futures:  # maybe `t` schuduled another task
                return
        # add waiter task if requested
        if get_waiter is not None:
            futures[get_waiter()] = None
        # execute tasks, and wait for one to fail or all to finish.
        # each task is independent from all other concurrent tasks
        # yield updates/debug output as each task finishes
        for t in tasks:
            if not t.writes:
                futures[
                    cast(
                        asyncio.Future,
                        self.submit(
                            arun_with_retry,
                            t,
                            retry_policy,
                            stream=self.use_astream,
                            writer=writer,
                            __name__=t.name,
                            __cancel_on_exit__=True,
                            __reraise_on_exit__=reraise,
                        ),
                    )
                ] = t
        done_futures: set[asyncio.Future] = set()
        end_time = timeout + loop.time() if timeout else None
        while len(futures) > (1 if get_waiter is not None else 0):
            done, inflight = await asyncio.wait(
                futures,
                return_when=asyncio.FIRST_COMPLETED,
                timeout=(max(0, end_time - loop.time()) if end_time else None),
            )
            if not done:
                break  # timed out
            for fut in done:
                task = futures.pop(fut)
                if task is None:
                    # waiter task finished, schedule another
                    if inflight and get_waiter is not None:
                        futures[get_waiter()] = None
                else:
                    # store for panic check
                    done_futures.add(fut)
                    # task finished, commit writes
                    self.commit(task, _exception(fut))
            else:
                # remove references to loop vars
                del fut, task
            # maybe stop other tasks
            if _should_stop_others(done):
                break
            # give control back to the caller
            yield
        # cancel waiter task
        for fut in futures:
            fut.cancel()
        # panic on failure or timeout
        _panic_or_proceed(
            done_futures.union(f for f, t in futures.items() if t is not None),
            timeout_exc_cls=asyncio.TimeoutError,
            panic=reraise,
        )

    def commit(
        self, task: PregelExecutableTask, exception: Optional[BaseException]
    ) -> None:
        if exception:
            if isinstance(exception, GraphInterrupt):
                # save interrupt to checkpointer
                if interrupts := [(INTERRUPT, i) for i in exception.args[0]]:
                    self.put_writes(task.id, interrupts)
            elif isinstance(exception, GraphDelegate):
                raise exception
            else:
                # save error to checkpointer
                self.put_writes(task.id, [(ERROR, exception)])
        else:
            if self.node_finished and (
                task.config is None or TAG_HIDDEN not in task.config.get("tags", [])
            ):
                self.node_finished(task.name)
            if not task.writes:
                # add no writes marker
                task.writes.append((NO_WRITES, None))
            # save task writes to checkpointer
            self.put_writes(task.id, task.writes)


def _should_stop_others(
    done: Union[set[concurrent.futures.Future[Any]], set[asyncio.Future[Any]]],
) -> bool:
    """Check if any task failed, if so, cancel all other tasks.
    GraphInterrupts are not considered failures."""
    for fut in done:
        if fut.cancelled():
            return True
        if exc := fut.exception():
            return not isinstance(exc, GraphInterrupt)
    else:
        return False


def _exception(
    fut: Union[concurrent.futures.Future[Any], asyncio.Future[Any]],
) -> Optional[BaseException]:
    """Return the exception from a future, without raising CancelledError."""
    if fut.cancelled():
        if isinstance(fut, asyncio.Future):
            return asyncio.CancelledError()
        else:
            return concurrent.futures.CancelledError()
    else:
        return fut.exception()


def _panic_or_proceed(
    futs: Union[set[concurrent.futures.Future], set[asyncio.Future]],
    *,
    timeout_exc_cls: Type[Exception] = TimeoutError,
    panic: bool = True,
) -> None:
    """Cancel remaining tasks if any failed, re-raise exception if panic is True."""
    done: set[Union[concurrent.futures.Future[Any], asyncio.Future[Any]]] = set()
    inflight: set[Union[concurrent.futures.Future[Any], asyncio.Future[Any]]] = set()
    for fut in futs:
        if fut.done():
            done.add(fut)
        else:
            inflight.add(fut)
    while done:
        # if any task failed
        if exc := _exception(done.pop()):
            # cancel all pending tasks
            while inflight:
                inflight.pop().cancel()
            # raise the exception
            if panic:
                raise exc
            else:
                return
    if inflight:
        # if we got here means we timed out
        while inflight:
            # cancel all pending tasks
            inflight.pop().cancel()
        # raise timeout error
        raise timeout_exc_cls("Timed out")
