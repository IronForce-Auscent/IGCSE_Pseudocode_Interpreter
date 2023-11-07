from core.interpreter import Interpreter

source = "13 + 12"
interpreter = Interpreter(source)
result = interpreter.expr()
print(result)