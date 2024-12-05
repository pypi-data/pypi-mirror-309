import asyncio
from threading import Thread
from typing import Any

from eclypse_core.remote.node.node import RemoteNode
from eclypse_core.remote.service import Service
from eclypse_core.remote.utils import (
    RemoteOps,
    ResponseCode,
)

class RemoteOpsThread(Thread):
    """Thread class for executing operations on a RemoteEngine.

    The operations are executed via the ops_entrypoint method of the Node class.
    """

    def __init__(self, node: RemoteNode, loop: asyncio.AbstractEventLoop) -> None:
        """Initializes the OpsThread class.

        Args:
            node (RemoteEngine): The node on which the operations will be executed.
            loop (asyncio.AbstractEventLoop): The event loop to run the operations.
        """

    def submit(self, engine_op: RemoteOps, op_args: dict):
        """Submits an operation to the OpsThread.

        Args:
            engine_op (RemoteOps): The operation to perform.
            op_args (Dict): The arguments for the operation.
        """

    def run(self) -> None:
        """Runs the thread to perform the operation on the service."""

    def deploy(self, service_id: str, service: Service) -> ResponseCode:
        """Deploys a service on the node.

        Args:
            service_id (str): The ID of the service to deploy.
            service (Service): The service to deploy.

        Returns:
            ResponseCode: The result of the operation: OK if successful, ERROR otherwise.
        """

    def undeploy(self, service_id: str) -> tuple[ResponseCode, Service | None]:
        """Undeploys a service from the node, retrieving the Service object.

        Args:
            service_id (str): The ID of the service to undeploy.

        Returns:
            Tuple[ResponseCode, Optional[Service]]: The result of the operation: (OK, service) if successful, (ERROR, None) otherwise.
        """

    def start_service(self, service_id: str) -> ResponseCode:
        """Starts a service on the node.

        Args:
            service_id (str): The ID of the service to start.

        Returns:
            ResponseCode: The result of the operation: OK if successful, ERROR otherwise.
        """

    def stop_service(self, service_id: str) -> ResponseCode:
        """Stops a service on the node.

        Args:
            service_id (str): The ID of the service to stop.

        Returns:
            ResponseCode: The result of the operation: OK if successful, ERROR otherwise.
        """

    async def set_future_result(self, future: asyncio.Future, result: Any):
        """Sets the result of the future. This method must be called to return the
        result of the operation to the caller.

        Args:
            future (asyncio.Future): The future to set the result.
            result (Any): The result of the operation.
        """
