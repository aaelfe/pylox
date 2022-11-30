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
        expr=self.logicalOr()

        if self.match(tt.EQUAL):
            equals=self.previous()
            value=self.assignment()

            if isinstance(expr, e.Variable):
                return e.Assign(expr.name, value)
            elif isinstance(expr, e.Get):
                get=expr
                return e.Set(get.obj, get.name, value)

            self.error(equals, "Invalid assignment target.")
        
        return expr

    def logicalOr(self):
        expr = self.logicalAnd()

        while self.match(tt.OR):
            operator=self.previous()
            right=self.logicalAnd()
            expr=e.Logical(expr, operator, right)

        return expr

    def logicalAnd(self):
        expr = self.equality()

        while self.match(tt.AND):
            operator=self.previous()
            right=self.equality()
            expr=e.Logical(expr, operator, right)

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
        return self.call()

    def call(self):
        expr=self.primary()

        while True:
            if self.match(tt.LEFT_PAREN):
                expr=self.finishCall(expr)
            elif self.match(tt.DOT):
                name=self.consume(tt.IDENTIFIER, "Expect property name after '.'.")
                expr = e.Get(expr, name)
            else:
                break

        return expr

    def finishCall(self, callee):
        arguments=[]

        if not self.check(tt.RIGHT_PAREN):
            flag=True
            while flag:
                arguments.append(self.expression())
                flag=self.match(tt.COMMA)

        paren=self.consume(tt.RIGHT_PAREN, "Expect ')' after arguments.")
        return e.Call(callee, paren, arguments)


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
            if self.match(tt.CLASS):
                return self.classDeclaration()
            if self.match(tt.FUN):
                return self.function("function")
            if self.match(tt.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def classDeclaration(self):
        name=self.consume(tt.IDENTIFIER, "Expect class name.")
        self.consume(tt.LEFT_BRACE, "Expect '{' before class body.")

        methods=[]
        while not self.check(tt.RIGHT_BRACE) and not self.tokens[self.current].tokenType==tt.EOF:
            methods.append(self.function("method"))

        self.consume(tt.RIGHT_BRACE, "Expect '}' after class body.")
        return s.Class(name, methods)

    def statement(self):
        if self.match(tt.FOR):
            return self.forStatement()
        if self.match(tt.IF):
            return self.ifStatement()
        if self.match(tt.PRINT):
            return self.printStatement()
        if self.match(tt.RETURN):
            return self.returnStatement()
        if self.match(tt.WHILE):
            return self.whileStatement()
        if self.match(tt.LEFT_BRACE):
            return s.Block(self.block())
        
        return self.expressionStatement()

    def returnStatement(self):
        keyword=self.previous()
        value=None
        if not self.check(tt.SEMICOLON):
            value=self.expression()
        
        self.consume(tt.SEMICOLON, "Expect ';' after return value.")
        return s.Return(keyword, value)

    def forStatement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer=None
        if self.match(tt.SEMICOLON):
            initializer=None
        elif self.match(tt.VAR):
            initializer=self.varDeclaration()
        else:
            initializer=self.expressionStatement()

        condition=None
        if not self.check(tt.SEMICOLON):
            condition=self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after loop condition.")

        increment=None
        if not self.check(tt.RIGHT_PAREN):
            increment=self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after for clauses.")

        body=self.statement()

        if increment is not None:
            body=s.Block([body, increment])

        if condition is None:
            condition=e.Literal(True)
            
        body=s.While(condition, body)

        if initializer is not None:
            body=s.Block([initializer, body])

        return body

    def whileStatement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'while'.")
        condition=self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after condition.")
        body=self.statement()
        return s.While(condition, body)

    def printStatement(self):
        value = self.expression()
        self.consume(tt.SEMICOLON, "Expect ';' after value.")
        return s.Print(value)

    def ifStatement(self):
        self.consume(tt.LEFT_PAREN, "Expect '(' after 'if'.")
        condition=self.expression()
        self.consume(tt.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = None

        if self.match(tt.ELSE):
            elseBranch=self.statement()

        return s.If(condition, thenBranch, elseBranch)

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

    def function(self, kind):
        name=self.consume(tt.IDENTIFIER, "Expect "+kind+" name.")
        self.consume(tt.LEFT_PAREN, "Expect '(' after "+kind+" name.")
        parameters=[]
        if not self.check(tt.RIGHT_PAREN):
            while True:
                parameters.append(self.consume(tt.IDENTIFIER, "Expect parameter name."))
                if not self.match(tt.COMMA):
                    break
        self.consume(tt.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(tt.LEFT_BRACE, "Expect '{' before "+kind+" body.")
        body=self.block()

        return s.Function(name, parameters, body)

    def block(self):
        statements = []
        while (not self.check(tt.RIGHT_BRACE)) and (not self.tokens[self.current].tokenType == tt.EOF):
            statements.append(self.declaration())
        self.consume(tt.RIGHT_BRACE, "Expect '}' after block.")
        return statements