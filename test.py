from core.parser import Parser
from core.lexer import Lexer
from core.interpreter import Interpreter

source = """
START
    LET x = 5;
    OUTPUT x;
END
"""
lexer = Lexer(source)
parser = Parser(lexer)
interpreter = Interpreter(parser)
interpreter.interpret()
print(interpreter.GLOBAL_SCOPE)