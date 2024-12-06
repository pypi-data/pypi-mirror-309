from typing import (
    Callable,
    Generator,
)

ConnectivityFn = Callable[
    [list[str], list[str]], Generator[tuple[str, str], None, None]
]
