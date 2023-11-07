from .token import Token, TokenType
import logging
import sys

class Interpreter(object):
    def __init__(self, source: str):
        """
        :param source: Source code written in pseudocode (str)
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.source: str = source 
        self.pos: int = 0
        self.cur_token: any = None
    
    def raise_exception(self, error_msg: str):
        """
        Throws a custom exception

        :param error_msg: The error message to be thrown (str)
        :return: N/A
        """
        self.logger.error(f"Interpreter error: {error_msg}")
        sys.exit("Exception thrown. Please reference interpreter logs for details")
    
    def get_next_token(self):
        """
        Lexical analyzer of the interpreter. Analyzes and breaks down source code into tokens

        :return: The token form of the source code (Token)
        """

        source = self.source
        if self.pos > len(source) - 1:
            return Token(TokenType.EOF, None)
        current_char = source[self.pos]
        while current_char in (" ", "\t", "\r"):
            self.pos += 1
            return self.get_next_token()

        if current_char.isdigit():
            token = Token(TokenType.INTEGER, int(current_char))
        elif current_char == "+":
            token = Token(TokenType.PLUS, current_char)
        elif current_char == "-":
            token = Token(TokenType.MINUS, current_char)
        else:
            self.raise_exception(f"Unidentified character found: {current_char}")
        self.pos += 1
        return token
    
    def eat(self, token_type: TokenType):
        """
        Compares the current token type with the token type passed, and consumes the current token if a match is found.
        Otherwise, an exception is raised
        """
        if self.cur_token.type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.raise_exception("Tokens do not match")

    def expr(self):
        """
        Parses an expression statement
        """
        result = None

        # Simple expression parsing for x + y
        self.cur_token = self.get_next_token()
        left = self.cur_token
        self.eat(TokenType.INTEGER)

        operator = self.cur_token # Expects a "+" operator
        if operator.value == "+":
            self.eat(TokenType.PLUS)
            right = self.cur_token
            self.eat(TokenType.INTEGER)
            result = left.value + right.value
        elif operator.value == "-":
            self.eat(TokenType.MINUS)
            right = self.cur_token
            self.eat(TokenType.INTEGER)
            result = left.value - right.value
        else:
            self.raise_exception(f"Unidentified character found: {operator}")
        return result