import enum

class TokenType(enum.Enum):
    # Format of token
    # name: value

    EOF = "EOF"
    NEWLINE = "NEWLINE"
    INTEGER = "INTEGER"
    IDENT = "IDENT"
    STRING = "STRING"
    BOOL = "BOOL"

    # Keywords
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    IF = "IF"
    THEN = "THEN"
    ENDIF = "ENDIF"
    WHILE = "WHILE"
    DO = "DO"
    ENDWHILE = "ENDWHILE"
    LET = "LET"
    FOR = "FOR"
    TO = "TO"
    NEXT = "NEXT"
    INCR = "INCR"
    DECR = "DECR"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # Operators
    EQ = "EQ"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    EQEQ = "EQEQ"
    NOTEQ = "NOTEQ"
    GTEQ = "GTEQ"
    GTHAN = "GTHAN"
    LTEQ = "LTEQ"
    LTHAN = "LTHAN"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"


class Token(object):
    def __init__(self, token_type: TokenType, token_value: any):        
        self.type: TokenType = token_type
        self.value: any = token_value
    
    def __str__(self):
        """
        Returns the string representation of the class instance

        :return: Token(self.type, self.value)
        """
        return f"Token({self.type}, {repr(self.value)})"
    
    def __repr__(self):
        return self.__str__()
