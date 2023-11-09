from .token import Token

class AST(object):
    pass

class BinOP(AST):
    def __init__(self, left: Token, operator: Token, right: Token):
        self.left: Token = left
        self.token = self.operator = operator
        self.right: Token = right

class Num(AST):
    def __init__(self, token: Token):
        self.token: Token = token
        self.value: any = self.token.value
    
