from loguru._logger import Logger

__all__ = ["Logger", "print_exception"]

def print_exception(e: Exception, raised_by: str):
    """Print the exception traceback and message.

    This is an internal function used to catch and print exception from asyncio tasks.

    Args:
        e (Exception): The exception raised.
        raised_by (str): The name of the function that raised the exception.
    """
