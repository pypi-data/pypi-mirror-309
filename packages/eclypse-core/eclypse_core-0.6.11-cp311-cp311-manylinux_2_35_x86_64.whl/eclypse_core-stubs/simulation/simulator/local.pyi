from concurrent.futures import Future
from enum import Enum
from typing import Any

from eclypse_core.graph import (
    Application,
    Infrastructure,
)
from eclypse_core.placement import (
    Placement,
    PlacementView,
)
from eclypse_core.placement.strategy import PlacementStrategy
from eclypse_core.report import Report
from eclypse_core.simulation.config import SimulationConfig
from eclypse_core.utils.logging import Logger

class Simulator:
    """The CallbackHandler class is used to manage the callbacks during the
    simulation."""

    def __init__(
        self, infrastructure: Infrastructure, simulation_config: SimulationConfig
    ) -> None:
        """Initialize the CallbackHandler object.

        Args:
            infrastructure (Infrastructure): The infrastructure to simulate.
            simulation_config (SimulationConfig): The simulation configuration.
        """

    def trigger(self, event_name: str, **kwargs) -> Future[dict[str, Any]] | None:
        """Triggers an external event (if possible, given the timeout and the max_calls
        parameters), scheduling its execution.

        Args:
            event_name (str): The name of the event to trigger.
            **kwargs: The arguments to pass to the event.

        Returns:
            Optional[Dict[str, Any]]: The result of the callbacks activated on the given event. If the event is not triggerable, None is returned.
        """

    def get_feed(self, event_name: str):
        """Get the feed for the given event.

        Args:
            event_name (str): The name of the event.

        Yields:
            Dict[str, Any]: The results of the event.
        """

    def start(self) -> None:
        """Start the simulation.

        Args:
            **kwargs: The additional arguments to pass to the start event.
        """

    async def run(self) -> None:
        """Run the simulation."""

    async def fire(
        self, event_name: str, triggered_by: str, future: Future | None = None, **kwargs
    ):
        """Fire the event."""

    def wait(self, timeout: float | None = None):
        """Wait for the simulation to finish.

        Args:
            timeout (Optional[float], optional): The maximum time to wait for the simulation to finish. Defaults to None, meaning indefinite wait.
        """

    def stop(self) -> None:
        """Stop the simulation.

        Args:
            blocking (bool, optional): Whether to block until the simulation stops. Defaults to True.
        """

    def cleanup(self) -> None:
        """Cleanup the simulation."""

    def get_report(self) -> Report | None:
        """Get the report of the simulation using the path provided in the
        configuration.

        Returns:
            Optional[Report]: The report of the simulation.
        """

    def register(
        self,
        application: Application,
        placement_strategy: PlacementStrategy | None = None,
    ):
        """Include an application in the simulation. A placement strategy must be
        provided.

        Args:
            application (Application): The application to include.
            placement_strategy (PlacementStrategy): The placement strategy to use.
        """

    def enact(self) -> None:
        """Enact the current placement of the applications onto the infrastructure."""

    @property
    def placements(self) -> dict[str, Placement]:
        """Get the placements of the applications in the simulation.

        Returns:
            Dict[str, Placement]: The placements of the applications.
        """

    @property
    def placement_view(self) -> PlacementView:
        """Get the placement view of the simulation.

        Returns:
            PlacementView: The placement view of the simulation.
        """

    @property
    def applications(self) -> list[Application]:
        """Get the applications included in the simulation.

        Returns:
            List[Application]: The list of Applications.
        """

    @property
    def logger(self) -> Logger:
        """Get the logger of the simulation.

        Returns:
            EclypseLogger: The logger of the simulation.
        """

    @property
    def status(self) -> SimulationState:
        """Get the state of the simulation.

        Returns:
            SimulationState: The state of the simulation.
        """

class SimulationState(Enum):
    """The state of the simulation."""

    IDLE = ...
    RUNNING = ...
    STOPPED = ...
