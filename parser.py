# from tokenType import TokenType
# from expr import Expr
# from lox import Lox
import tokenType
import expr as e
import lox
import stmt as s

tt = tokenType.TokenType

class RuntimeException():
    def __init__(self, message):
        self.message=message

class ParseError(Exception):
    pass

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr=self.equality()

        if self.match(tt.EQUAL):
            equals=self.previous()
            value=self.assignment()

            if isinstance(expr, e.Variable):
                return e.Assign(expr.name, value)

            self.error(equals, "Invalid assignment target.")
        
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(tt.BANG_EQUAL, tt.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = e.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(tt.GREATER, tt.GREATER_EQUAL, tt.LESS, tt.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = e.Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(tt.MINUS, tt.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = e.Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(tt.SLASH, tt.STAR):
            operator = self.previous()
            right = self.unary()
            expr = e.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(tt.BANG, tt.MINUS):
            operator = self.previous()
            right = self.unary()
            return e.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(tt.FALSE):
            return e.Literal(False)
        if self.match(tt.TRUE):
            return e.Literal(True)
        if self.match(tt.NIL):
            return e.Literal(None)

        if self.match(tt.NUMBER, tt.STRING):
            return e.Literal(self.previous().literal)

        if self.match(tt.IDENTIFIER):
            return e.Variable(self.previous())

        if self.match(tt.LEFT_PAREN):
            expr = self.expression()
            # print(expr+" <-EXPR")
            self.consume(tt.RIGHT_PAREN, "Expect ')' after expression.")
            return e.Grouping(expr)
        raise self.error(self.tokens[self.current], "Expect expression.")

    def match(self, *tokenTypes):
        for tokenType in tokenTypes:
            if self.check(tokenType):
                self.advance()
                return True
        return False

    def consume(self, tokenType, message):
        if self.check(tokenType):
            #print("in consume")
            return self.advance()
        raise self.error(self.tokens[self.current], message)

    def check(self, tokenType):
        if self.tokens[self.current].tokenType == tt.EOF:
            #print("in check")
            return False
        return self.tokens[self.current].tokenType == tokenType

    def advance(self):
        if not self.tokens[self.current].tokenType == tt.EOF:
            self.current=self.current+1
        return self.previous()

    def previous(self):
        return self.tokens[self.current-1]

    def error(self, token, message):
        l = lox.Lox()
        l.parseError(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.tokens[self.current].tokenType == tt.EOF:
            if self.previous().tokenType == tt.SEMICOLON:
                return
        if self.tokens[self.current].tokenType in [tt.CLASS, tt.FUN, tt.VAR, tt.FOR, tt.IF, tt.WHILE, tt.PRINT, tt.RETURN]:
            return
        self.advance()

    def parse(self):
        statements=[]
        while not self.tokens[self.current].tokenType == tt.EOF:
            statements.append(self.declaration())

        return statements

    def declaration(self):
        try:
            if self.match(tt.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match(tt.PRINT):
            return self.printStatement()
        
        return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after value.")
        return s.Print(value)

    def varDeclaration(self):
        name = self.consume(tt.IDENTIFIER, "Expect variable name.")
        initializer = None

        if self.match(tt.EQUAL):
            initializer=self.expression()

        self.consume(tt.SEMICOLON, "Expect ';' after variable declaration.")
        return s.Var(name, initializer)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after expression.")
        return s.Expression(expr)