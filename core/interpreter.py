from .exception import ExceptionHandler
from .nodevisitor import NodeVisitor
from .token import Token, TokenType
from .parser import Parser
from .ast import BinOP, UnaryOP
import logging

class Interpreter(NodeVisitor):
    """
    Interpreter class to execute source code with help from the Parser class

    :param parser: The parser used to parse the tokens
    :type parser: Parser()
    """
    def __init__(self, parser: Parser):
        self.parser: Parser = parser
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.ExceptionHandler: ExceptionHandler = ExceptionHandler(__name__)    
    
    def visit_BinOP(self, node: BinOP) -> any:
        """
        Traverses the left and right nodes and evaluates based on the operator type of the current node

        :param node: The current node
        :type node: BinOP()
        :return: Evaluated results
        :rtype: any
        """
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        else:
            pass  # Placeholder
    
    def visit_Num(self, node: Token) -> any:
        """
        Traverses and returns the value of the node passed as argument

        :param node: The node to get the value of
        :type node: Token()
        :return: The associated value with the node
        :rtype: any
        """
        return node.value
    
    def visit_UnaryOP(self, node: UnaryOP) -> any:
        op = node.op.type
        if op == TokenType.PLUS:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS:
            return -self.visit(node.expr)
        else:
            pass # Placeholder

    def interpret(self) -> any:
        """
        Interprets the source code

        :return: Results from executing source code
        :rtype: any
        """
        tree = self.parser.parse()
        return self.visit(tree)