from typing import Generator

from eclypse_core.graph import (
    Application,
    Infrastructure,
)
from eclypse_core.placement import Placement
from eclypse_core.placement.strategy import PlacementStrategy
from eclypse_core.utils.logging import Logger

class PlacementManager:
    """PlacementManager manages the placement of applications in the infrastructure."""

    def __init__(
        self, infrastructure: Infrastructure, incremental_mapping_phase: bool = False
    ) -> None:
        """Initializes the PlacementManager.

        Args:
            infrastructure (Infrastructure): The infrastructure to place the applications onto.
            incremental_mapping_phase (bool, optional): If True, the placement is done incrementally,
                i.e. one application at a time. If False, the placement is done in batch.
                Defaults to False.
        """

    def enact(self) -> None:
        """Enact the current placement of the applications onto the infrastructure."""

    def tick(self) -> None:
        """Iterates over the placements of all the involved applications."""

    def generate_mapping(self, placement: Placement):
        """Generate the mapping of the applications onto the infrastructure, using the
        placement strategy if available. If no placement strategy is available, the
        global one is used.

        Args:
            placement (Placement): The placement to generate the mapping for.
        """

    def mapping_phase(
        self,
    ) -> (
        list[tuple[Placement, list[str]]]
        | Generator[tuple[Placement, list[str]], None, None]
    ):
        """Executes the mapping phase of the placement of the applications onto the
        infrastructure. If the placement is incremental, it will return a generator of
        tuples containing the placement and the nodes that are not respected by the
        placement. If the placement is not incremental, it will return a list of such
        tuples.

        Returns:
            Union[
                List[Tuple[Placement, List[str]]],
                Generator[Tuple[Placement, List[str]], None, None],
            ]: A list of tuples containing the placement and the nodes that are not respected by the placement, or a generator of such tuples.
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

    def get(self, application_id: str) -> Placement:
        """Get the placement of an application.

        Args:
            application_id (str): The ID of the application.

        Returns:
            Placement: The placement of the application,

        Raises:
            KeyError: If the application is not found.
        """

    @property
    def logger(self) -> Logger:
        """Get a logger for the PlacementManager.

        Returns:
            Logger: The logger for the PlacementManager.
        """
