from .service import Service

class RESTService(Service):
    """Base class for services in ECLYPSE remote applications."""

    def __init__(self, service_id: str) -> None:
        """Initializes a Service object.

        Args:
            service_id (str): The name of the service.
        """

    @property
    def mpi(self) -> None:
        """Raises an error since the service is not an MPI service.

        Raises:
            RuntimeError: The service is not an MPI service.
        """
