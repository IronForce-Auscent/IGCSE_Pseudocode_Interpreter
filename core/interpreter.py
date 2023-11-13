from .exception import ExceptionHandler
from .nodevisitor import NodeVisitor
from .token import Token, TokenType
from .parser import Parser
from .ast import *
import logging

class Interpreter(NodeVisitor):
    """
    Interpreter class to execute source code with help from the Parser class

    :param parser: The parser used to parse the tokens
    :type parser: Parser()
    """

    GLOBAL_SCOPE = {}

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

    def visit_Compound(self, node: Compound):
        """
        Iterates through each child node and visits them

        :param node: The compound node
        :type node: Compound()
        """
        for child in node.children:
            self.visit(child)

    def visit_NoOP(self, noce: NoOP):
        pass
    
    def visit_Assign(self, node: Assign):
        """
        Traverses through an assignment node and stores its value in a dictionary as a key-value pair

        :param node: The assignment node
        :type node: Assign()
        """
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node: Variable) -> any:
        """
        Traverses through a variable node and performs a lookup of the variable name in the global scope. If a match is
        found, the corrosponding value is returned. Otherwise, a NameError exception is thrown

        :param node: The variable node
        :type node: Variable()
        :return: The corrosponding value associated with the variable
        :rtype: any
        """
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val


    def interpret(self) -> any:
        """
        Interprets the source code

        :return: Results from executing source code
        :rtype: any
        """
        tree = self.parser.parse()
        return self.visit(tree)