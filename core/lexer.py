from .token import Token, TokenType
from .exception import ExceptionHandler
import logging

class Lexer(object):
    def __init__(self, source: str):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.ExceptionHandler: ExceptionHandler = ExceptionHandler(__name__)
        self.source: str = source
        self.pos: int = 0
        self.cur_char: str | int | any = self.source[self.pos]

    def skip_whitespaces(self):
        while self.cur_char is not None and self.cur_char.isspace():
            self.advance()
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.source) - 1:
            self.cur_char = None
            self.logger.info("Reached end of source code")
        else:
            self.cur_char = self.source[self.pos]

    def integer(self) -> int:
        """
        Returns a multidigit integer consumed from the input

        :rtype: int
        """
        result = ""
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token(TokenType, any):
        """
        Lexical analyzer of the interpreter. Analyzes and breaks down source code into tokens

        :return: The token form of the source code
        :rtype: Token()
        """
        while self.cur_char is not None:
            if self.cur_char.isspace():
                self.skip_whitespaces()
                continue
    
            if self.cur_char.isnumeric():
                token = Token(TokenType.INTEGER, self.integer())
            elif self.cur_char == "+":
                token = Token(TokenType.PLUS, self.cur_char)
                self.advance()
            elif self.cur_char == "-":
                token = Token(TokenType.MINUS, self.cur_char)
                self.advance()
            elif self.cur_char == "*":
                token = Token(TokenType.MUL, self.cur_char)
                self.advance()
            elif self.cur_char == "/":
                token = Token(TokenType.DIV, self.cur_char)
                self.advance()
            elif self.cur_char == "(":
                token = Token(TokenType.LPAREN, self.cur_char)
                self.advance()
            elif self.cur_char == ")":
                token = Token(TokenType.RPAREN, self.cur_char)
                self.advance()
            else:
                self.ExceptionHandler.raise_exception(f"Unidentified character found: {self.cur_char}")
            return token
        return Token(TokenType.EOF, None)