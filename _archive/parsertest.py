from core.lexer import Lexer
from core.token import TokenType
from core.parser import Parser
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Compiler requires source file as argument")
    with open(sys.argv[1], "r") as f:
        source = f.read()
    
    lexer = Lexer(source)
    parser = Parser(lexer)
    parser.program()
    print("Parsing completed")

if __name__ == "__main__":
    main()