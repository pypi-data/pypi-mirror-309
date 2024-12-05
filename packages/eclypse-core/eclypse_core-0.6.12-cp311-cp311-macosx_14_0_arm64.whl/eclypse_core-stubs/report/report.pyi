from pathlib import Path

import datapane as dp

from eclypse_core.utils._logging import Logger
from eclypse_core.utils.types import PlotType

DEFAULT_HTML_REPORT_FILENAME: str
DEFAULT_TICK_COLUMN: str
REPORT_ACCENT_COLOR: str
SIMULATION_PAGE_TITLE: str
APPLICATION_PAGE_TITLE: str
INFRASTRUCTURE_PAGE_TITLE: str

class Report:
    """The Report class generates the final report of the simulation."""

    step: int
    loaded: bool
    def __init__(self, sim_path: Path | str) -> None:
        """Create a new Report with default values.

        Args:
            sim_path (str): The path to the simulation.
        """

    def load_stats(self, report_range: tuple[int, int] = ..., report_step: int = 1):
        """Load the statistics of the simulation from the configured path.

        Args:
            report_range (Tuple[int, int], optional): The range of ticks to include
                in the report. Defaults to (0, MAX_FLOAT).
            report_step (int, optional): The step between report ticks. Defaults to 1.
        """

    def to_csv(self, path: str | None = None):
        """Save the reports in CSV format.

        Args:
            path (Optional[str], optional): The path to save the CSV reports.
                Defaults to None.
        """

    def to_json(self, path: str | None = None):
        """Save the reports in JSON format.

        Args:
            path (Optional[str], optional): The path to save the JSON reports.
                Defaults to None.
        """

    def to_html(
        self,
        path: str | None = None,
        plot_types: dict[str, PlotType] | None = None,
        open_html: bool = False,
    ):
        """Save the reports in HTML format.

        Args:
            path (Optional[str], optional): The path to save the HTML report.
                Defaults to None.
            plot_types (Optional[Dict[str, PlotType]], optional): The plot types for each
                metric. Defaults to None.
            open_html (bool, optional): Whether to open the HTML report in the default
                browser. Defaults to False.
        """

    def simulation_page(self) -> dp.Page:
        """Create the simulation metrics page.

        Returns:
            dp.Page: The simulation metrics page.
        """

    def applications_page(self, plot_types: dict[str, PlotType]) -> dp.Page:
        """Create the applications page with all the application metrics, for each
        applicationnvolved in the simulation. Also includes the service and interaction
        metrics.

        Returns:
            dp.Page: The applications page.
        """

    def infrastructure_page(self, plot_types: dict[str, PlotType]) -> dp.Page:
        """Create the infrastructure page with all the infrastructure metrics. Also
        includes the node and link metrics.

        Returns:
            dp.Page: The infrastructure page.
        """

    def gml_page(self) -> dp.Page:
        """Create the network page with the network graph.

        Returns:
            dp.Page: The network page.
        """

    @property
    def logger(self) -> Logger:
        """Get the logger of the Report, binding the id to "Report".

        Returns:
            Logger: The logger of the Report.
        """
