from . import lexer
from .token import Token, TokenType
import sys
import logging

class Parser():
    """
    The parser will keep track of the current token and check if the code matches the expected grammar
    """
    def __init__(self, lexer: lexer.Lexer):
        self.lexer = lexer # Initialize the lexer
        self.logger = logging.getLogger(__name__)

        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token() # This is called twice to initialize both the current and the peek tokens
        

    def check_token(self, kind: TokenType):
        """
        Returns if the token provided is valid

        Arguments:
        kind (TokenType): The token type of the current token

        Returns:
        _ (bool): Whether the provided kind matches the token kind of the current token
        """
        return kind == self.cur_token.kind

    def check_peek(self, kind: TokenType):
        """
        Returns if the next token provided is valid
        
        Arguments:
        kind (TokenType): The token type of the current token

        Returns:
        _ (bool): Whether the provided kind matches the token kind of the next token
        """
        return kind == self.peek_token.kind

    def match(self, kind: TokenType):
        """
        Try to match the current token
        If it doesn't match, return an error
        Advance the current token

        Arguments:
        kind (TokenType): The token type of the current token
        """
        if not self.check_token(kind):
            self.abort(f"Expected {kind.name}, got {self.cur_token.kind.name} instead")
        self.next_token()

    def next_token(self):
        """
        Advances the current token
        """
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token() # EOF characters will be handled by the Lexer

    def abort(self, message: str):
        self.logger.error(f"Parsing error: {message}")
        sys.exit("Parsing error, please check the generated logs for more information")

    # Past this point, we will parse all the tokens according to the grammar rules we specified in grammar/syntax.txt
    # Each rule will be given its own grammar

    def program(self):
        """
        Processes the grammar rule "<prgm> ::= <stmt>
        """
        self.logger.info("PROGRAM")

        # It would be smart if we could process whitespaces at the start too, so lets do that
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
            
        # Parse all the other statements in the program, exit if we get an EOF
        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        """
        Processes the grammar rule "<stmt> ::= (...)
        """
        # This is by far the most complex function due to how many statements are allowed in the grammar of the language
        # To do this, we will check the first token of each statement to determine what kind of statement we're dealing with

        # Statement: "OUTPUT" <expr | string>
        if self.check_token(TokenType.OUTPUT):
            self.logger.info("STATEMENT-OUTPUT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                # Looks like we found the string we want to print out...
                self.next_token()
            else:
                # If it is not a string, then it should be an expression
                self.expression()
        # Statement: "IF" <condi> "THEN" nl {<expr>} nl "ENDIF"
        elif self.check_token(TokenType.IF):
            self.logger.info("STATEMENT-IF")
            self.next_token()
            self.comparison()
            self.match(TokenType.THEN) # Checks for end of comparison
            self.newline()

            # Check for zero or more statements in body
            while not self.check_token(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
        
        # Statement: "WHILE" <condi> "DO" nl {<expr>} nl "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            self.logger.info("STATEMENT-WHILE")
            self.next_token()
            self.comparison()
            self.match(TokenType.DO) # Checks for end of condition
            self.newline()

            # Check for zero or more statements in body
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
        
        # Statement: "INPUT" <ident>
        elif self.check_token(TokenType.INPUT):
            self.logger.info("STATEMENT-INPUT")
            self.next_token()
            self.match(TokenType.IDENT)
        
        # Statement: "LET" <ident> "=" <expr | string | bool>
        elif self.check_token(TokenType.LET):
            self.logger.info("STATEMENT-LET")
            self.next_token()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            """
            # To be implemented in the future, for now this will only support exprs
            if self.check_token(TokenType.STRING):
                self.next_token()
            elif self.check_token(TokenType.BOOL):
                self.boolean()
            else:
                self.expression()
            """
            self.expression()
        
        # Statement: "GOTO" <ident>
        elif self.check_token(TokenType.GOTO):
            self.logger.info("STATEMENT-GOTO")
            self.next_token()
            self.match(TokenType.IDENT)
        
        # Statement: "LABEL" <ident>
        elif self.check_token(TokenType.LABEL):
            self.logger.info("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)

        
        # Not a valid expression, throw an error!
        else:
            self.abort(f"Invalid statement at {self.cur_token.text} ({self.cur_token.kind.name})")

        self.newline()

    
    def newline(self):
        """
        Processes the grammar rule "<nl> ::= '\n'+"
        """
        self.logger.info("NEWLINE")

        # Requires at least one newline
        self.match(TokenType.NEWLINE)
        # But we do accept multiple newlines, so let's check for them too
        while self.check_peek(TokenType.NEWLINE):
            self.next_token()
