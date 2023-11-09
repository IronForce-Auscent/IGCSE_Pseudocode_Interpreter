from typing import Literal
import sys
import logging

class ExceptionHandler():
    def __init__(self, source: Literal["Interpreter", "Parser", "Lexer"]):
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