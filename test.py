from core.interpreter import Interpreter

source = "5 * 5 - 5 / 5 + 5 / 5"
interpreter = Interpreter(source)
result = interpreter.expr()
print(result)