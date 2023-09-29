from .token import Token, TokenType
import sys

TOKENTYPE = TokenType

class Lexer():
    def __init__(self, source):
        self.source = source
        self.curChar = "" # The current character that the lexer is scanning
        self.curPos = -1 # The current position in the code that the lexer is scanning
        self.nextChar()
    
    def nextChar(self):
        """
        Processes the next character in the code
        """
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0" # Returns an EOF character
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        """
        Returns the lookahead character
        """
        if self.curPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.curPos + 1]

    def abort(self, message: str):
        """
        Exits compiler with an error message if an invalid token is found

        Arguments:
        message (str): The error message to output
        """
        sys.exit(f"Lexing error: {message}")

    def skipWhitespace(self):
        """
        Skips all whitespaces except newline characters

        Newline characters are used to indicate end of statement
        """
        while self.curChar == ' ' or self.curChar == "\t" or self.curChar == "\r":
            self.nextChar()

    def skipComment(self):
        """
        Skips all comments
        """
        if self.curChar == "/" and self.peek() == "/":
            while self.curChar != "\n":
                self.nextChar()

    def getToken(self) -> Token:
        """
        Classifies and returns the next token
        """
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "\"":
            # Get the characters between the double quotations
            self.nextChar()
            startPos = self.curPos

            while self.curChar != "\"":
                # Restrict all special characters (eg escape, newline, tabs, %)
                # Makes it easier to compile to C later on
                if self.curChar in ["\r", "\n", "\t", "\\", "%"]:
                    self.abort("Illegal character in string")
                self.nextChar()

            tokenText = self.source[startPos:self.curPos] # Get the substring
            token = Token(tokenText, TokenType.STRING)
        elif self.curChar == "=":
            # Check whether the token is = or ==
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            # Check whether the token is > or >=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GTHAN)
        elif self.curChar == "<":
            # Check whether the token is < or <=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LTHAN)
        elif self.curChar == "!":
            # Check whether the token is ! or !=
            # If the token is !, return an error
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort(f"!= expected, got !{self.peek()}")
        
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)

        elif self.curChar.isdigit():
            # Leading character is a digit, so it should be a number
            # Check the consecutive digits and check if there is a decimal
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".": # Its a decimal
                self.nextChar()

                # There must be at least another digit after the decimal
                if not self.peek().isdigit():
                    # Error found!
                    self.abort("Illegal character in number")
                while self.peek().isdigit():
                    self.nextChar()
            tokenText = self.source[startPos:self.curPos + 1]
            token = Token(tokenText, TokenType.NUMBER)
        else:
            self.abort(f"Unknown token found: {self.curChar}")

        self.nextChar()
        return token