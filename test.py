from core.parser import Parser
from core.lexer import Lexer

source = "IF 5 * ((1 + (1 + 1)) + (1 + 1))"
lexer = Lexer(source)
parser = Parser(lexer)
result = parser.expr()
print(result)