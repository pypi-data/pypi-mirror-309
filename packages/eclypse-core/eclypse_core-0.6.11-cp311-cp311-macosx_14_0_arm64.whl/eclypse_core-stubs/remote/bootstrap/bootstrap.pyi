from eclypse_core.graph.infrastructure import Infrastructure
from eclypse_core.remote.node import RemoteNode
from eclypse_core.simulation.config import SimulationConfig
from eclypse_core.simulation.simulator.remote import RemoteSimulator

from .options_factory import RayOptionsFactory

class RemoteBootstrap:
    """Configuration for the remote infrastructure."""

    def __init__(
        self,
        sim_class: type[RemoteSimulator] | None = None,
        node_class: type[RemoteNode] | None = None,
        ray_options_factory: RayOptionsFactory | None = None,
        resume_if_exists: bool = False,
        **node_args
    ) -> None:
        """Create a new RemoteConfig with default values.

        Args:
            node_config (Dict[str, Any], optional): The configuration to be passed to remote nodes in initialization. Defaults to {}.
            node_affinity_label (str, optional): The affinity label for instantiating remote nodes on specific nodes of the cluster. Defaults to None.
            ray_options (Dict[str, Any], optional): Additional Ray options. Defaults to
                {}.
        """

    def build(
        self,
        infrastructure: Infrastructure,
        simulation_config: SimulationConfig | None = None,
    ):
        """Build the remote simulation."""
