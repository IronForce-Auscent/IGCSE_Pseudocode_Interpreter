import enum

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords (101 - 200)
    INPUT = 101
    OUTPUT = 102
    IF = 103
    THEN = 104
    ENDIF = 105
    WHILE = 106
    DO = 107
    ENDWHILE = 108
    LET = 109
    FOR = 110
    TO = 111
    NEXT = 112
    INCR = 113
    DECR = 114
    TRUE = 115
    FALSE = 116

    # Operators (201 - 300)
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    GTEQ = 208
    GTHAN = 209
    LTEQ = 210
    LTHAN = 211


class Token:
    def __init__(self, tokenText: str, tokenKind: any):
        self.text = tokenText
        self.kind = tokenKind
    
    @staticmethod
    def checkIfKeyword(tokenText: str) -> TokenType | None:
        for kind in TokenType:
            if kind.name == tokenText and kind.value > 100 and kind.value < 300:
                return kind
        return None