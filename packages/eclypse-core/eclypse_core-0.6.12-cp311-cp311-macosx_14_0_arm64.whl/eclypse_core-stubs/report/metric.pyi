from typing import Callable

from eclypse_core.utils.types import CallbackType
from eclypse_core.workflow.callbacks import EclypseCallback

class EclypseMetric(EclypseCallback):
    def __init__(
        self,
        name: str,
        callback_type: CallbackType | None = None,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = "csv",
        aggregate_fn: str | Callable | None = None,
        remote: bool = False,
    ) -> None: ...

class EclypseMetricWrapper(EclypseMetric):
    def __init__(
        self,
        callback_fn: Callable,
        name: str,
        callback_type: CallbackType,
        activates_on: str | list[str] = "tick",
        activates_every_n: dict[str, int] | None = None,
        triggers: dict[str, Callable] | None = None,
        report: str | list[str] | None = "csv",
        aggregate_fn: str | Callable | None = None,
        remote: bool = False,
    ) -> None: ...
    def __call__(self, *args, **kwargs): ...
