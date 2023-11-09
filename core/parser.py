from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOP, Num
from .nodevisitor import NodeVisitor
from .exception import ExceptionHandler
import logging

class Parser(NodeVisitor):
    def __init__(self, lexer: Lexer):
        """
        :param source: Source code written in pseudocode
        :type source: str
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.ExceptionHandler: ExceptionHandler = ExceptionHandler(__name__)
        self.lexer: Lexer = lexer
        self.cur_token: Token = self.lexer.get_next_token()
    
    def visit_BinOP(self, node: BinOP):
        """
        Traverses the left and right nodes and evaluates based on the operator type of the current node

        :param node: The current node
        :type node: BinOP()
        :return: Evaluated results
        :rtype: any
        """
        if node.operator.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operator.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operator.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.operator.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        else:
            pass  # Placeholder
    
    def visit_Num(self, node: Token):
        """
        Traverses and returns the value of the node passed as argument

        :param node: The node to get the value of
        :type node: Token()
        :return: The associated value with the node
        :rtype: any
        """
        return node.value
    
    def eat(self, token_type: TokenType):
        """
        Compares the current token type with the token type passed, and consumes the current token if a match is found.
        Otherwise, an exception is raised
        """
        if self.cur_token.type == token_type:
            self.cur_token = self.lexer.get_next_token()
        else:
            self.logger.error(f"Token 1: {self.cur_token.type}. Token 2: {token_type}")
            self.ExceptionHandler.raise_exception("Tokens do not match")

    def factor(self) -> Num | BinOP:
        """
        Parses a factor statement
        Ruleset: <factor> ::= <int> | <LPAREN> <expr> <RPAREN>

        :return: Evaluation result(s)
        :rtype: Node() | Num()
        """
        token: Token = self.cur_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self) -> BinOP:
        """
        Parses a term statement
        Rulset: <term> ::= <factor> {("/" | "*") <factor>}

        :return: Evaluation result(s)
        :rtype: Node()
        """
        node = self.factor()
        while self.cur_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.cur_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            else:
                pass # Placeholder
            node = BinOP(left=node, operator=token, right=self.factor())
        return node


    def expr(self) -> BinOP:
        """
        Parses an expression statement
        Ruleset: <expr> ::= <term> {("-" | "+") <term>}

        :return: Evaluation result(s)
        :rtype: Node()
        """
        # Simple expression parsing for x + y
        node = self.term()
        while self.cur_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.cur_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            else:
                pass # Placeholder
            node = BinOP(left=node, operator=token, right=self.factor())
        return node

    def parse(self) -> BinOP:
        """
        Calls and returns an expression

        :return: Evaluation result(s)
        :rtype: any
        """
        return self.expr()