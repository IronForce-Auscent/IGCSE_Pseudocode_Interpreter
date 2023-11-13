from .token import Token, TokenType
from .exception import ExceptionHandler
import logging

class Lexer(object):
    """
    Lexical analyzer ("Lexer") class to convert raw source code into tokens

    :param source: Source code written in pseudocode, according to the syntax defined in the BNF syntax document
    :type source: str
    """
    def __init__(self, source: str):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.ExceptionHandler: ExceptionHandler = ExceptionHandler(__name__)
        self.source: str = source
        self.pos: int = 0
        self.cur_char: str | int | any = self.source[self.pos]

    def skip_whitespaces(self):
        """
        Skips whitespaces and tabs in the code
        """
        while self.cur_char is not None and self.cur_char.isspace():
            self.advance()
    
    def advance(self):
        """
        Advances to the next character in the code
        """
        self.pos += 1
        if self.pos > len(self.source) - 1:
            self.cur_char = None
            self.logger.info("Reached end of source code")
        else:
            self.cur_char = self.source[self.pos]

    def peek(self) -> any:
        """
        Performs a lookahead action at the next character in the source code without modifying
        its current position, and returns the following character's value

        :return: The next character in the source code
        """
        peek_pos = self.pos + 1
        if peek_pos > len(self.source) - 1:
            return None
        else:
            return self.source[peek_pos]

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
    
    def _id(self) -> Token(any, str):
        """
        Handles reserved keywords and identifiers

        :return: Token form of the keyword/identifier
        :rtype: Token()
        """
        result = ""
        while self.cur_char is not None and self.cur_char.isalnum():
            result += self.cur_char
            self.advance()
        token = Token(TokenType.get_token_type(result), TokenType.get_values(result, ""))
        return token

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

            if self.cur_char.isalpha():
                return self._id()

            if self.cur_char == "=":
                token = Token(TokenType.EQ, self.cur_char)
                self.advance()
                return token

            if self.cur_char == ";":
                token = Token(TokenType.SEMI, self.cur_char)
                self.advance()
                return token
            
            if self.cur_char == ".":
                token = Token(TokenType.DOT, self.cur_char)
                self.advance()
                return token

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