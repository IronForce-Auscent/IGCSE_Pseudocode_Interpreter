import sys
import logging

class ExceptionHandler():
    """
    Custom exceptions handler to handle errors found during runtime in the interpreter

    :param source: The current script that has initialized the function (recommended to use __name__ when initializing)
    :type source: str
    """
    def __init__(self, source: str):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.source: str = source

    def raise_exception(self, error_msg: str):
        """
        Throws a custom exception

        :param source: The source of the exception (Accepts only )
        :type source: str
        :param error_msg: The error message to be thrown
        :type error_msg: str
        :return: N/A
        """
        self.logger.error(f"{self.source} error: {error_msg}")
        sys.exit("Exception thrown. Please reference interpreter logs for details")