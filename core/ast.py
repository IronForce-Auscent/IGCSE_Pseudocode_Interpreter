from .token import Token

class AST(object):
    """
    Base abstract syntax tree (AST) node class
    """
    pass

class BinOP(AST):
    """
    Binary operator node

    eg. BinOP(left=Token(TokenType.INTEGER, 5), op=Token(TokenType.PLUS, "+"), right=Token(TokenType.INTEGER, 7))

    :param left: Left operand
    :type left: Token()
    :param op: Binary operator being used
    :type op: Token()
    :param right: Right operand
    :type right: Token()
    """
    def __init__(self, left: Token, op: Token, right: Token):
        self.left: Token = left
        self.token = self.op = op
        self.right: Token = right

class Num(AST):
    """
    Numerical node to represent integers

    :param token: Token of integer to be represented
    :type token: Token()
    """
    def __init__(self, token: Token):
        self.token: Token = token
        self.value: any = self.token.value
    
class UnaryOP(AST):
    """
    Unary operator node

    :param op: Unary operator being used
    :type op: Token()
    :param expr: The expression representing the right operand
    :type expr: BinOP() | UnaryOP() | Num()
    """
    def __init__(self, op: Token, expr: BinOP | Num):
        self.token = self.op = op
        self.expr = expr