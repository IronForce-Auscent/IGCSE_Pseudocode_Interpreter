from .token import Token
import logging

class NodeVisitor(object):
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(__name__)

    def visit(self, node: Token):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor
    
    def generic_visit(self, node):
        self.logger.error(f"No visit_{type(node).__name__} method")
    
