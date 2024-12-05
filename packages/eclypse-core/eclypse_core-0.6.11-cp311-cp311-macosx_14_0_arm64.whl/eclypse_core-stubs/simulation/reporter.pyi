from pathlib import Path

from eclypse_core.report.reporter import Reporter
from eclypse_core.workflow.callbacks import EclypseCallback

class SimulationReporter:
    """Class to report the simulation reportable callbacks."""

    def __init__(
        self, report_path: str | Path, reporters: dict[str, type[Reporter]]
    ) -> None:
        """Create a new SimulationReporter, initializing the CSV, GML, and TensorBoard
        reporters.

        Args:
            report_path (Union[str, Path]): The path to save the reports.
        """

    def report(self, event_name: str, event_idx: int, executed: list[EclypseCallback]):
        """Report the simulation reportable callbacks, thus writing them according to
        the reporter type.

        Args:
            event_name (str): The name of the event.
            event_idx (int): The index of the event trigger (tick).
            executed (List[EclypseCallback]): The executed callbacks.

        Raises:
            ValueError: If the reporter type is not supported.
        """
