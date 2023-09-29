from interpreter.lexer import Lexer
from interpreter.token import TokenType

def main():
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

if __name__ == "__main__":
    main()