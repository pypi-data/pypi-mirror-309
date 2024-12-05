from eclypse_core.placement import Placement

class RemoteSimOpsHandler:
    """A RemoteSimOpsHandler performs the operations on the remote nodes.

    Available operations are: deploy, start, stop and undeploy.
    """

    @staticmethod
    def deploy(placement: Placement):
        """Deploy the services to the remote nodes, according to the placement mapping.

        Args:
            placement (Placement): The placement mapping of the services to the nodes.

        Raises:
            ValueError: If any of the responses from the remote nodes is an error.
        """

    @staticmethod
    def start(placement: Placement):
        """Start the deployed services on the remote nodes.

        Args:
            placement (Placement): The placement mapping of the services to the nodes.

        Raises:
            ValueError: If any of the responses from the remote nodes is an error.
        """

    @staticmethod
    def stop(placement: Placement):
        """Stop the running services on the remote nodes.

        Args:
            placement (Placement): The placement mapping of the services to the nodes.

        Raises:
            ValueError: If any of the responses from the remote nodes is an error.
        """

    @staticmethod
    def undeploy(placement: Placement):
        """Undeploy the services from the remote nodes.

        Args:
            placement (Placement): The placement mapping of the services to the nodes.

        Raises:
            ValueError: If any of the responses from the remote nodes is an error.
        """
