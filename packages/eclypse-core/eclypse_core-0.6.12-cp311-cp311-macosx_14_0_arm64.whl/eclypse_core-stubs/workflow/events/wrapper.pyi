from typing import (
    Any,
    Callable,
)

from .event import EclypseEvent

class EventWrapper(EclypseEvent):
    def __init__(
        self,
        event_fn: Callable,
        name: str,
        trigger_every_ms: float | None = None,
        timeout: float | None = None,
        max_calls: int | None = None,
        triggers: dict[str, str | int | list[int]] | None = None,
        verbose: bool = False,
    ) -> None: ...
    def __call__(self, **kwargs) -> dict[str, Any]: ...
