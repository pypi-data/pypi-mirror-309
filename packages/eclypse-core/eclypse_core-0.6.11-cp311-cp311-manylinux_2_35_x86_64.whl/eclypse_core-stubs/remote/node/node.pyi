import asyncio
from typing import (
    Any,
    Callable,
)

from eclypse_core.remote.communication import Route
from eclypse_core.remote.service import Service
from eclypse_core.remote.utils import RemoteOps
from eclypse_core.utils.logging import Logger

class RemoteNode:
    """Base class for a node in the infrastructure, implemented as a Ray actor."""

    def __init__(self, node_id: str, infrastructure_id: str, **node_config) -> None:
        """Initializes the Node.

        Args:
            node_id (str): The name of the node.
            infrastructure_id (str): The ID of the infrastructure.
            **node_config: The configuration of the node.
        """

    def build(self, **node_config) -> None:
        """Performs the setup of the node's environment when the node is instantiated
        within the infrastructure.

        The build method and has a twofold purpose.

        **Define object-level attributes**. This encloses attributes that are independent
        from whether the node is executing the training method or the test method (e.g.,
        choosing the optimizer, the loss function, etc.).

        **Perform all the resource-intensive operations in advance to avoid bottlenecks**.
        An example can be downloading the data from an external source, or instantiating
        a model with computationally-intensive techniques.

        Since it is called within the ``__init__`` method, the user can define additional
        class attributes.

        An example of build function can be the following:

        .. code-block:: python

            def build(self, dataset_name: str):
                self._dataset_name = dataset_name
                self._dataset = load_dataset(self._dataset_name)
        """

    async def ops_entrypoint(self, engine_op: RemoteOps, **op_args) -> Any:
        """Entry point for executing operations involving services within a node.
        Currently, the operations implemented are `DEPLOY`, `UNDEPLOY`, `START` and
        `STOP`. If none of these operations are specified,

        Args:
            service_id (str): The ID of the service.
            fn (str): The functionality to be executed.
            **fn_args: The arguments of the function to be invoked.
        """

    async def entrypoint(self, service_id: str | None, fn: Callable, **fn_args) -> Any:
        """Entry point for executing functions within a node. If service_id is None, the
        function is executed in the node itself.

        Args:
            service_id (str): The ID of the service.
            fn (str): The functionality to be executed.
            **fn_args: The arguments of the function to be invoked.
        """

    async def service_comm_entrypoint(
        self, route: Route, comm_interface: type, **handle_args
    ) -> Any:
        """Entry point for the communication interface of a service deployed in the
        node. It is used to allow the interaction among services by leveraging the Ray
        Actor\'s remote method invocation.

        Args:
            service_id (str): The ID of the service.
            comm_interface (str): The communication interface to be used. Currently, only "EclypseMPI" and "EclypeREST" are supported.
            **handle_args: The arguments of the function to be invoked.
        """

    @property
    def id(self) -> str:
        """Returns the node's full ID."""

    @property
    def infrastructure_id(self) -> str:
        """Returns the infrastructure ID."""

    @property
    def services(self) -> dict[str, Service]:
        """Returns the dictionary of services deployed in the node."""

    @property
    def engine_loop(self) -> asyncio.AbstractEventLoop:
        """Returns the asyncio event loop of the node."""

    @property
    def logger(self) -> Logger:
        """Returns the logger of the node."""
