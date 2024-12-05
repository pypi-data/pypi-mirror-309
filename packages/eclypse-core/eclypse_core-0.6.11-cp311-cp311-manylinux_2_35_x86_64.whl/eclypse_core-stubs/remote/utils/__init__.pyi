from typing import Any

import ray

from .ops import RemoteOps
from .response_code import ResponseCode

__all__ = ["ray_get", "RemoteOps", "ResponseCode"]

def ray_get(obj: ray.ObjectRef) -> Any | list[Any]:
    """Get the result of a Ray task or a list of Ray tasks, ignoring any output to
    stderr.

    Args:
        Any: The Ray task or list of Ray tasks.

    Returns:
        Union[Any, List[Any]]: The result of the Ray task or list of Ray tasks.
    """
