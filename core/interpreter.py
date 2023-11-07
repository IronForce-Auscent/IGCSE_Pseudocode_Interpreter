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
        self.cur_char = source[self.pos]
        
        self.allowed_operators = (
            TokenType.PLUS, 
            TokenType.MINUS,
            TokenType.ASTERISK, 
            TokenType.SLASH
        )
    
    def raise_exception(self, error_msg: str):
        """
        Throws a custom exception

        :param error_msg: The error message to be thrown (str)
        :return: N/A
        """
        self.logger.error(f"Interpreter error: {error_msg}")
        sys.exit("Exception thrown. Please reference interpreter logs for details")

    #######################################################################
    #                                                                     #
    #                   Lexical Analyzer logic                            #
    #                                                                     #
    #######################################################################

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

    def integer(self):
        """
        Returns a multidigit integer consumed from the input

        :return: integer
        """
        result = ""
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        Lexical analyzer of the interpreter. Analyzes and breaks down source code into tokens

        :return: The token form of the source code (Token)
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
                token = Token(TokenType.ASTERISK, self.cur_char)
                self.advance()
            elif self.cur_char == "/":
                token = Token(TokenType.SLASH, self.cur_char)
                self.advance()
            else:
                self.raise_exception(f"1 Unidentified character found: {self.cur_char}")
            return token
        return Token(TokenType.EOF, None)
    
    #######################################################################
    #                                                                     #
    #                   Parser/Component logic                            #
    #                                                                     #
    #######################################################################
    
    def eat(self, token_type: TokenType):
        """
        Compares the current token type with the token type passed, and consumes the current token if a match is found.
        Otherwise, an exception is raised
        """
        if self.cur_token.type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.raise_exception("Tokens do not match")

    def term(self):
        """
        Parses and returns a token value of token type INTEGER

        :return: Token value (int)
        """
        token = self.cur_token
        self.eat(TokenType.INTEGER)
        return token.value

    def expr(self):
        """
        Parses an expression statement
        """

        # Simple expression parsing for x + y
        self.cur_token = self.get_next_token()
        result = self.term()
        while self.cur_token.type in self.allowed_operators:
            token = self.cur_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
            elif token.type == TokenType.ASTERISK:
                self.eat(TokenType.ASTERISK)
                result *= self.term()
            elif token.type == TokenType.SLASH:
                self.eat(TokenType.SLASH)
                result /= self.term()
            else:
                pass # Placeholder
        else:
            if self.cur_token.type != TokenType.EOF:
                self.raise_exception(f"Unexpected expression: {self.cur_token.value}")
        return result