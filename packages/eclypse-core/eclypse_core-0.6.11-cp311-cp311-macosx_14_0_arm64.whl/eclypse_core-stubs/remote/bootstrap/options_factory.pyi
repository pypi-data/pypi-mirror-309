from typing import Any

class RayOptionsFactory:
    """Factory for creating Ray options for remote actors."""

    def __init__(self, detached: bool = False, **std_options) -> None:
        """Create a new RayOptionsFactory.

        Args:
            detached (bool, optional): Whether to run the actor detached. Defaults to False.
            **std_options: The standard options to use.
        """

    def __call__(self, name: str) -> dict[str, Any]:
        """Create the options for the actor.

        Args:
            name (str): The name of the actor.

        Returns:
            Dict[str, Any]: The options for the actor.
        """
