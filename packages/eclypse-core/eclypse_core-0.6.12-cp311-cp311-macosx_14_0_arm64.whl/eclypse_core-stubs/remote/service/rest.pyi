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
        """Returns the EclypseMPI interface of the service."""
