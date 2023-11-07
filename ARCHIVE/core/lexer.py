from .token import Token, TokenType
import sys
import logging

class Lexer():
    def __init__(self, source):
        self.source = source
        self.logger = logging.getLogger(__name__)
        self.cur_char = "" # The current character that the lexer is scanning
        self.cur_pos = -1 # The current position in the code that the lexer is scanning
        self.get_next_character()
    
    def get_next_character(self):
        """
        Processes the next character in the code
        """
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = "\0" # Returns an EOF character
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        """
        Returns the lookahead character
        """
        if self.cur_pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.cur_pos + 1]

    def raise_exception(self, message: str):
        """
        Throws a custom exception

        :param error_msg: The error message to be thrown (str)
        :return: N/A
        """
        self.logger.error(f"Lexing error: {message}")
        sys.exit("Lexing error, please check the generated logs for more information")

    def skip_whitespace(self):
        """
        Skips all whitespaces except newline characters

        Newline characters are used to indicate end of statement
        """
        while self.cur_char == ' ' or self.cur_char == "\t" or self.cur_char == "\r":
            self.get_next_character()

    def skip_comment(self):
        """
        Skips all comments
        """
        if self.cur_char == "/" and self.peek() == "/":
            while self.cur_char != "\n":
                self.get_next_character()

    def get_next_token(self) -> Token:
        """
        Classifies and returns the next token
        """
        self.skip_whitespace()
        self.skip_comment()
        token = None

        if self.cur_char == "+":
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == "-":
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == "*":
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == "/":
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == "\"":
            # Get the characters between the double quotations
            self.get_next_character()
            startPos = self.cur_pos

            while self.cur_char != "\"":
                # Restrict all special characters (eg escape, newline, tabs, %)
                # Makes it easier to compile to C later on
                if self.cur_char in ["\r", "\n", "\t", "\\", "%"]:
                    self.raise_exception("Illegal character in string")
                self.get_next_character()

            tokenText = self.source[startPos:self.cur_pos] # Get the substring
            token = Token(tokenText, TokenType.STRING)
        elif self.cur_char == "=":
            # Check whether the token is = or ==
            if self.peek() == "=":
                lastChar = self.cur_char
                self.get_next_character()
                token = Token(lastChar + self.cur_char, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)
        elif self.cur_char == ">":
            # Check whether the token is > or >=
            if self.peek() == "=":
                lastChar = self.cur_char
                self.get_next_character()
                token = Token(lastChar + self.cur_char, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.GTHAN)
        elif self.cur_char == "<":
            # Check whether the token is < or <=
            if self.peek() == "=":
                lastChar = self.cur_char
                self.get_next_character()
                token = Token(lastChar + self.cur_char, TokenType.LTEQ)
            else:
                token = Token(self.cur_char, TokenType.LTHAN)
        elif self.cur_char == "!":
            # Check whether the token is ! or !=
            # If the token is !, return an error
            if self.peek() == "=":
                lastChar = self.cur_char
                self.get_next_character()
                token = Token(lastChar + self.cur_char, TokenType.NOTEQ)
            else:
                self.raise_exception(f"!= expected, got !{self.peek()}")
        
        elif self.cur_char == "\n":
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == "\0":
            token = Token(self.cur_char, TokenType.EOF)

        elif self.cur_char.isdigit():
            # Leading character is a digit, so it should be a number
            # Check the consecutive digits and check if there is a decimal
            startPos = self.cur_pos
            while self.peek().isdigit():
                self.get_next_character()
            if self.peek() == ".": # Its a decimal
                self.get_next_character()

                # There must be at least another digit after the decimal
                if not self.peek().isdigit():
                    # Error found!
                    self.raise_exception("Illegal character in number")
                while self.peek().isdigit():
                    self.get_next_character()
            tokenText = self.source[startPos:self.cur_pos + 1]
            token = Token(tokenText, TokenType.NUMBER)
        elif self.cur_char.isalpha():
            # Leading character is a letter, so it should be a string
            # Get consecutive alpha-numeric characters
            startPos = self.cur_pos
            while self.peek().isalpha():
                self.get_next_character()
            tokenText = self.source[startPos:self.cur_pos + 1] # Get substring
            keyword = Token.checkIfKeyword(tokenText) # Check if there are any keywords within the string
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)

        else:
            self.raise_exception(f"Unknown token found: {self.cur_char}")

        self.get_next_character()
        return token