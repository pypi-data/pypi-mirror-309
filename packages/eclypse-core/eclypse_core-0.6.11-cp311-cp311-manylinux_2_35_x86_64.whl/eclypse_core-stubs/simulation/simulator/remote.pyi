from typing import Any

from eclypse_core.remote.communication.route import Route

from .local import Simulator

class RemoteSimulator(Simulator):
    """The RemoteSimulator is used to implement a remote simulation of the
    infrastructural conditions.

    When a service needs to interact with another service, it communicates with the
    RemoteSimulator to define the current costs for such interaction.
    """

    def __init__(self, *args, **kwargs) -> None: ...
    def enact(self) -> None:
        """Enacts the placements within the remote infrastructure."""

    async def trigger(self, event_name: str, **kwargs) -> dict[str, Any] | None:
        """Triggers an event in the simulation."""

    async def get_feed(self, event_name: str): ...
    async def wait(self, timeout: float | None = None):
        """Wait for the simulation to finish."""

    def cleanup(self) -> None: ...
    async def route(
        self, application_id: str, source_id: str, dest_id: str
    ) -> Route | None:
        """Computes the route between two logically neighbor services. If the services
        are not logically neighbors, it returns None.

        Args:
            source_id (str): The ID of the source service.
            dest_id (str): The ID of the destination service.

        Returns:
            Route: The route between the two services.
        """

    async def get_neighbors(self, application_id: str, service_id: str) -> list[str]:
        """Returns the logical neighbors of a service in an application.

        Args:
            service_id (str): The ID of the service for which to retrieve the neighbors.

        Returns:
            List[str]: A list of service IDs.
        """

    def get_status(self):
        """Returns the status of the simulation."""

    @property
    def id(self) -> str:
        """Returns the ID of the infrastructure manager."""

    @property
    def remote(self) -> bool:
        """Returns True if the simulation is remote, False otherwise."""
