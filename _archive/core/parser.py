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

        self.symbols = set()  # Stores a list of variables initialized so far
        self.labels_declared = set()   # Stores a list of labels declared so far
        self.labels_gotoed = set()    # Stores a list of labels we have goto'd so far   

        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token() # This is called twice to initialize both the current and the peek tokens
        

    def check_token(self, kind: TokenType):
        """
        Returns if the token provided is valid

        :param kind: The token type of the current token (TokenType)

        :return: Whether the provided kind matches the token kind of the current token (bool)
        """
        return kind == self.cur_token.type

    def check_peek(self, kind: TokenType):
        """
        Returns if the next token provided is valid
        
        :param kind: The token type of the current token (TokenType)

        :return: Whether the provided kind matches the token kind of the next token (bool)
        """
        return kind == self.peek_token.kind

    def match(self, kind: TokenType):
        """
        Try to match the current token
        If it doesn't match, return an error
        Advance the current token

        :param kind: The token type of the current token (TokenType)
        """
        if not self.check_token(kind):
            self.abort(f"Expected {kind.name}, got {self.cur_token.type.name} instead")
        self.next_token()
        
    def is_comparison_operator(self):
        """
        Checks if the current token is a comparison operator ("==", ">=", ">", "<=", "<", "!=")

        :return: Whether the current token is a comparison operator or not (bool)
        """
        return self.check_token(TokenType.GTHAN) or self.check_token(TokenType.GTEQ) or self.check_token(TokenType.LTHAN) or self.check_token(TokenType.LTEQ) or self.check_token(TokenType.EQEQ) or self.check_token(TokenType.NOTEQ)

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

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort(f"Attempting to GOTO undefined label: {label}")

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
            self.match(TokenType.THEN)  # Checks for end of comparison
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

            if self.cur_token.value not in self.symbols:
                # Check if the variable has already been defined. If not, define it
                self.symbols.add(self.cur_token.value)

            self.match(TokenType.IDENT)
        
        # Statement: "LET" <ident> "=" <expr | string | bool>
        elif self.check_token(TokenType.LET):
            self.logger.info("STATEMENT-LET")
            self.next_token()

            if self.cur_token.value not in self.symbols:
                # Check if the variable has already been defined. If not, define it
                self.symbols.add(self.cur_token.value)

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

            self.labels_gotoed.add(self.cur_token.value)  # Adds the current label to the list
            self.match(TokenType.IDENT)
        
        # Statement: "LABEL" <ident>
        elif self.check_token(TokenType.LABEL):
            self.logger.info("STATEMENT-LABEL")
            self.next_token()

            if self.cur_token.value in self.labels_declared:
                # Looks like this label has already been declared, lets give the user an error
                self.abort(f"Label already exists: {self.cur_token.value}")

            self.labels_declared.add(self.cur_token.value)
            self.match(TokenType.IDENT)

        
        # Not a valid expression, throw an error!
        else:
            self.abort(f"Invalid statement at {self.cur_token.value} ({self.cur_token.type.name})")

        self.newline()

    
    def newline(self):
        """
        Processes the grammar rule "<nl> ::= '\n'+"
        """
        self.logger.info("NEWLINE")

        # Requires at least one newline
        self.match(TokenType.NEWLINE)
        # But we do accept multiple newlines, so let's check for them too
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def comparison(self):
        """
        Processes the grammar rule "<condi> ::= <expr> ("==" | ">" | ">=" | "<" | "<=" | "!=") <expr>"
        """
        self.logger.info("COMPARISON")

        self.expression()
        # Statement must contain at least one comparison operator and another expression
        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort(f"Expected expression operator at: {self.cur_token.value}")
        
        # We can allow 0 or more comparison operators and expressions afterwards
        while self.is_comparison_operator():
            self.next_token()
            self.expression()
    
    def expression(self):
        """
        Processes the grammar rule "<expr> ::= <term> {("-" | "+") <term>}"
        """
        self.logger.info("EXPRESSION")

        self.term()
        # We can have 0 or more +/- operators and terms
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()
    
    def term(self):
        """
        Processes the grammar rule "<term> ::= <factor> {("/" | "*") <factor>}"
        """
        self.logger.info("TERM")

        self.factor()
        # We can have 0 or more //* operators and factors
        while self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.next_token()
            self.factor()
    
    def factor(self):
        """
        Processes the grammar rule "<factor> ::= ["+" | "-"] <primary>"
        """
        self.logger.info("FACTOR")

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    def primary(self):
        """
        Processes the grammar rule "<primary> ::= <number> | <ident>"
        """
        self.logger.info(f"PRIMARY: {self.cur_token.value}")

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            # Ensure that the variable already exists
            if self.cur_token.value not in self.symbols:
                self.abort(f"Attempting to reference variable before assignment: {self.cur_token.value}")
            self.next_token()
        else:
            # Invalid assigned value, throw an error
            self.abort(f"Unexpected token at: {self.cur_token.value}")