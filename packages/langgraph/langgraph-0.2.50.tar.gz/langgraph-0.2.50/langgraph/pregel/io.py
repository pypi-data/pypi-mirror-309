from typing import Any, Iterator, Literal, Mapping, Optional, Sequence, TypeVar, Union
from uuid import UUID

from langchain_core.runnables.utils import AddableDict

from langgraph.channels.base import BaseChannel, EmptyChannelError
from langgraph.constants import (
    EMPTY_SEQ,
    ERROR,
    FF_SEND_V2,
    INTERRUPT,
    NULL_TASK_ID,
    PUSH,
    RESUME,
    TAG_HIDDEN,
    TASKS,
)
from langgraph.pregel.log import logger
from langgraph.types import Command, PregelExecutableTask, Send


def is_task_id(task_id: str) -> bool:
    """Check if a string is a valid task id."""
    try:
        UUID(task_id)
    except ValueError:
        return False
    return True


def read_channel(
    channels: Mapping[str, BaseChannel],
    chan: str,
    *,
    catch: bool = True,
    return_exception: bool = False,
) -> Any:
    try:
        return channels[chan].get()
    except EmptyChannelError as exc:
        if return_exception:
            return exc
        elif catch:
            return None
        else:
            raise


def read_channels(
    channels: Mapping[str, BaseChannel],
    select: Union[Sequence[str], str],
    *,
    skip_empty: bool = True,
) -> Union[dict[str, Any], Any]:
    if isinstance(select, str):
        return read_channel(channels, select)
    else:
        values: dict[str, Any] = {}
        for k in select:
            try:
                values[k] = read_channel(channels, k, catch=not skip_empty)
            except EmptyChannelError:
                pass
        return values


def map_command(
    cmd: Command,
) -> Iterator[tuple[str, str, Any]]:
    """Map input chunk to a sequence of pending writes in the form (channel, value)."""
    if cmd.send:
        if isinstance(cmd.send, (tuple, list)):
            sends = cmd.send
        else:
            sends = [cmd.send]
        for send in sends:
            if not isinstance(send, Send):
                raise TypeError(
                    f"In Command.send, expected Send, got {type(send).__name__}"
                )
            yield (NULL_TASK_ID, PUSH if FF_SEND_V2 else TASKS, send)
    if cmd.resume:
        if isinstance(cmd.resume, dict) and all(is_task_id(k) for k in cmd.resume):
            for tid, resume in cmd.resume.items():
                yield (tid, RESUME, resume)
        else:
            yield (NULL_TASK_ID, RESUME, cmd.resume)
    if cmd.update:
        if not isinstance(cmd.update, dict):
            raise TypeError(
                f"Expected cmd.update to be a dict mapping channel names to update values, got {type(cmd.update).__name__}"
            )
        for k, v in cmd.update.items():
            yield (NULL_TASK_ID, k, v)


def map_input(
    input_channels: Union[str, Sequence[str]],
    chunk: Optional[Union[dict[str, Any], Any]],
) -> Iterator[tuple[str, Any]]:
    """Map input chunk to a sequence of pending writes in the form (channel, value)."""
    if chunk is None:
        return
    elif isinstance(input_channels, str):
        yield (input_channels, chunk)
    else:
        if not isinstance(chunk, dict):
            raise TypeError(f"Expected chunk to be a dict, got {type(chunk).__name__}")
        for k in chunk:
            if k in input_channels:
                yield (k, chunk[k])
            else:
                logger.warning(f"Input channel {k} not found in {input_channels}")


class AddableValuesDict(AddableDict):
    def __add__(self, other: dict[str, Any]) -> "AddableValuesDict":
        return self | other

    def __radd__(self, other: dict[str, Any]) -> "AddableValuesDict":
        return other | self


def map_output_values(
    output_channels: Union[str, Sequence[str]],
    pending_writes: Union[Literal[True], Sequence[tuple[str, Any]]],
    channels: Mapping[str, BaseChannel],
) -> Iterator[Union[dict[str, Any], Any]]:
    """Map pending writes (a sequence of tuples (channel, value)) to output chunk."""
    if isinstance(output_channels, str):
        if pending_writes is True or any(
            chan == output_channels for chan, _ in pending_writes
        ):
            yield read_channel(channels, output_channels)
    else:
        if pending_writes is True or {
            c for c, _ in pending_writes if c in output_channels
        }:
            yield AddableValuesDict(read_channels(channels, output_channels))


class AddableUpdatesDict(AddableDict):
    def __add__(self, other: dict[str, Any]) -> "AddableUpdatesDict":
        return [self, other]

    def __radd__(self, other: dict[str, Any]) -> "AddableUpdatesDict":
        raise TypeError("AddableUpdatesDict does not support right-side addition")


def map_output_updates(
    output_channels: Union[str, Sequence[str]],
    tasks: list[tuple[PregelExecutableTask, Sequence[tuple[str, Any]]]],
    cached: bool = False,
) -> Iterator[dict[str, Union[Any, dict[str, Any]]]]:
    """Map pending writes (a sequence of tuples (channel, value)) to output chunk."""
    output_tasks = [
        (t, ww)
        for t, ww in tasks
        if (not t.config or TAG_HIDDEN not in t.config.get("tags", EMPTY_SEQ))
        and ww[0][0] != ERROR
        and ww[0][0] != INTERRUPT
    ]
    if not output_tasks:
        return
    if isinstance(output_channels, str):
        updated = (
            (task.name, value)
            for task, writes in output_tasks
            for chan, value in writes
            if chan == output_channels
        )
    else:
        updated = (
            (
                task.name,
                {chan: value for chan, value in writes if chan in output_channels},
            )
            for task, writes in output_tasks
            if any(chan in output_channels for chan, _ in writes)
        )
    grouped: dict[str, list[Any]] = {t.name: [] for t, _ in output_tasks}
    for node, value in updated:
        grouped[node].append(value)
    for node, value in grouped.items():
        if len(value) == 0:
            grouped[node] = None  # type: ignore[assignment]
        if len(value) == 1:
            grouped[node] = value[0]
    if cached:
        grouped["__metadata__"] = {"cached": cached}  # type: ignore[assignment]
    yield AddableUpdatesDict(grouped)


T = TypeVar("T")


def single(iter: Iterator[T]) -> Optional[T]:
    for item in iter:
        return item
