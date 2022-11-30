import expr as e
import stmt as s
import lox as l
from enum import Enum, auto

class FunctionType(Enum):
    NONE=auto()
    FUNCTION=auto()
    METHOD=auto()

class Resolver(e.Visitor, s.Visitor):
    def __init__(self, interpreter):
        self.interpreter=interpreter
        self.scopes=[]
        self.currentFunction=FunctionType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolveBlock(stmt.statements)
        self.endScope()

    def visitClassStmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        for method in stmt.methods:
            declaration=FunctionType.METHOD
            self.resolveFunction(method, declaration)

    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolveExpression(stmt.initializer)
        self.define(stmt.name)

    def visitFunctionStmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)

    def visitExpressionStmt(self, stmt):
        self.resolveExpression(stmt.expression)

    def visitIfStmt(self, stmt):
        self.resolveExpression(stmt.condition)
        self.resolveStatement(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolveStatement(stmt.elseBranch)

    def visitPrintStmt(self, stmt):
        self.resolveExpression(stmt.expression)

    def visitReturnStmt(self, stmt):
        if self.currentFunction==FunctionType.NONE:
            l.parseError(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolveExpression(stmt.value)

    def visitWhileStmt(self, stmt):
        self.resolveExpression(stmt.condition)
        self.resolveStatement(stmt.body)

    def visitVariableExpr(self, expr):
        if len(self.scopes)!=0 and self.scopes[-1].get(expr.name.lexeme) is False:
            l.parseError(expr.name, "Can't read local variable in its own initializer.")
        self.resolveLocal(expr, expr.name)

    def visitAssignExpr(self, expr):
        self.resolveExpression(expr.value)
        self.resolveLocal(expr, expr.name)

    def visitBinaryExpr(self, expr):
        self.resolveExpression(expr.left)
        self.resolveExpression(expr.right)

    def visitCallExpr(self, expr):
        self.resolveExpression(expr.callee)
        for argument in expr.arguments:
            self.resolveExpression(argument)

    def visitGetExpr(self, expr):
        self.resolveExpression(expr.obj)

    def visitSetExpr(self, expr):
        self.resolveExpression(expr.value)
        self.resolveExpression(expr.obj)

    def visitGroupingExpr(self, expr):
        self.resolveExpression(expr.expression)

    def visitLiteralExpr(self, expr):
        pass

    def visitLogicalExpr(self, expr):
        self.resolveExpression(expr.left)
        self.resolveExpression(expr.right)

    def visitUnaryExpr(self, expr):
        self.resolveExpression(expr.right)

    def resolveLocal(self, expr, name):
        for i in reversed(range(len(self.scopes))):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes)-1-i)
                return

    def resolveFunction(self, function, type):
        enclosingFunction=self.currentFunction
        self.currentFunction=type

        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolveBlock(function.body)
        self.endScope()

        self.currentFunction=enclosingFunction

    def resolveBlock(self, statements):
        for statement in statements:
            self.resolveStatement(statement)

    def resolveStatement(self, statement):
        statement.accept(self)

    def resolveExpression(self, expression):
        expression.accept(self)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes)==0:
            return
        scope=self.scopes[-1]
        if name.lexeme in scope.keys():
            l.parseError(name, "Already a variable with this name in this scope.")
        scope[name.lexeme]=False

    def define(self, name):
        if len(self.scopes)==0:
            return
        self.scopes[-1][name.lexeme]=True