from core.parser import Parser
from core.lexer import Lexer
from core.interpreter import Interpreter

source = "5 - - - 2"
lexer = Lexer(source)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(result)