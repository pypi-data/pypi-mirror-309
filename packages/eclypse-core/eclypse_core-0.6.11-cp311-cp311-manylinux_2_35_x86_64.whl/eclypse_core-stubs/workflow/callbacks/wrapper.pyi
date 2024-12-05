from typing import (
    Any,
    Callable,
)

from eclypse_core.utils.types import CallbackType

from .callback import EclypseCallback

class CallbackWrapper(EclypseCallback):
    def __init__(
        self,
        callback_fn: Callable,
        name: str,
        callback_type: CallbackType | None = None,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = "csv",
        remote: bool = False,
    ) -> None: ...
    def __call__(self, *args, **kwargs) -> dict[str, Any]: ...
