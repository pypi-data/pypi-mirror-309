from enum import StrEnum

class HTTPMethod(StrEnum):
    """HTTP methods supported by the `EclypseREST` communication interface.

    Attributes:
        GET: The GET HTTP method.
        POST: The POST HTTP method.
        PUT: The PUT HTTP method.
        DELETE: The DELETE HTTP method.
    """

    GET = ...
    POST = ...
    PUT = ...
    DELETE = ...
