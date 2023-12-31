from .token import Token, TokenType
from .lexer import Lexer
from .ast import *
from .nodevisitor import NodeVisitor
from .exception import ExceptionHandler
import logging

class Parser(NodeVisitor):
    """
    Parser class to process the tokens generated by the lexer 

    :param lexer: The lexical analyzer used
    :type lexer: Lexer()
    """
    def __init__(self, lexer: Lexer):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.ExceptionHandler: ExceptionHandler = ExceptionHandler(__name__)
        self.lexer: Lexer = lexer
        self.cur_token: Token = self.lexer.get_next_token()
    
    def eat(self, token_type: TokenType):
        """
        Compares the current token type with the token type passed, and consumes the current token if a match is found.
        Otherwise, an exception is raised
        """
        if self.cur_token.type == token_type:
            self.cur_token = self.lexer.get_next_token()
        else:
            self.logger.error(f"Token 1: {self.cur_token.type}; Token 2: {token_type}")
            self.ExceptionHandler.raise_exception("Tokens do not match")
    
    def program(self) -> any:
        """
        Parses the program statement
        Ruleset: <prgm> ::= <compound>

        :return: 
        :rtype:
        """
        node = self.compound()
        return node
    
    def compound(self) -> Compound:
        """
        Parses compound statements
        Ruleset: <compound> ::= START <stmt_list> END

        :return:
        :rtype: Compound()
        """
        self.eat(TokenType.START)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        
        return root
    
    def statement_list(self) -> list:
        """
        Parses statement lists (consecutive statements)
        Ruleset: <stmt_list> ::= <stmt> | <stmt> <stmt_list>

        :return:
        :rtype: list
        """
        node = self.statement()
        results = [node]

        while self.cur_token.type != TokenType.EOF:
            self.eat(TokenType.SEMI)
            results.append(self.statement())
        
        if self.cur_token.type == TokenType.IDENTIFIER:
            self.ExceptionHandler.raise_exception(f"Unexpected identifier: {self.cur_token.value}")
        
        return results
    
    def statement(self) -> Assign | Compound | NoOP:
        """
        Parses a statement
        Ruleset: <stmt> ::= <compound> 
            | <assignment>
            | <empty>
        
        :return:
        :rtype: Assign() | Compound() | NoOP()
        """
        if self.cur_token.type == TokenType.START:
            node = self.compound()
        elif self.cur_token.type == TokenType.IDENTIFIER:
            node = self.assignment()
        else:
            node = self.empty()
        return node
    
    def assignment(self) -> Assign:
        """
        Parses an assignment statement
        Ruleset: <assignment> ::= LET <var> = <expr>

        :rtype: Assign()
        """
        left = self.variable()
        token = self.cur_token()
        self.eat(TokenType.EQ)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self) -> Variable:
        """
        Parses a variable statement
        Ruleset: <var> ::= <identifier>

        :rtype: Variable()
        """
        node = Variable(self.cur_token)
        self.eat(TokenType.IDENTIFIER)
        return node
    
    def empty(self) -> NoOP:
        """
        Parses an empty statement
        Ruleset: None

        :rtype: NoOP()
        """
        return NoOP()

    def factor(self) -> Num | BinOP | Variable:
        """
        Parses a factor statement
        Ruleset: <factor> ::= [("-" | "+")] <factor> | <int> | <LPAREN> <expr> <RPAREN> | <var>

        :return: Evaluation result(s)
        :rtype: BinOP() | Num()
        """
        token: Token = self.cur_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOP(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOP(token, self.factor())
            return node
        elif token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self) -> BinOP:
        """
        Parses a term statement
        Rulset: <term> ::= <factor> {("/" | "*") <factor>}

        :return: Evaluation result(s)
        :rtype: BinOP()
        """
        node = self.factor()
        while self.cur_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.cur_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            else:
                pass # Placeholder
            node = BinOP(left=node, op=token, right=self.factor())
        return node


    def expr(self) -> BinOP:
        """
        Parses an expression statement
        Ruleset: <expr> ::= <term> {("-" | "+") <term>}

        :return: Evaluation result(s)
        :rtype: BinOP()
        """
        # Simple expression parsing for x + y
        node = self.term()
        while self.cur_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.cur_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            else:
                pass # Placeholder
            node = BinOP(left=node, op=token, right=self.factor())
        return node

    def parse(self) -> BinOP:
        """
        Calls and returns an expression

        :return: Evaluation result(s)
        :rtype: BinOP()
        """
        node = self.program()
        if self.cur_token.type != TokenType.EOF:
            self.ExceptionHandler.raise_exception(f"EOF character expected, got {self.cur_token.type} instead")

        return node