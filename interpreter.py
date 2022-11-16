import expr as e
import stmt as s
import tokenType
import lox
import runtimeError
import environment

tt = tokenType.TokenType

class Interpreter(e.Visitor, s.Visitor):
    def __init__(self):
        self.environment = environment.Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except runtimeError.RuntimeE as error:
            self.error(error)

    def error(self, e):
        l=lox.Lox()
        l.runtimeError(e)

    def execute(self, stmt):
        stmt.accept(self)

    def stringify(self, object):
        if object is None:
            return "nil"

        if isinstance(object, bool):
            text=str(object).lower()
            return text

        if isinstance(object, float):
            text=str(object)
            if text.endswith(".0"):
                text=text[:-2]
            return text

        return str(object)

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.tokenType == tt.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)-float(right)
        elif expr.operator.tokenType == tt.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)/float(right)
        elif expr.operator.tokenType == tt.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)*float(right)
        elif expr.operator.tokenType == tt.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left)+float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left)+str(right)
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.tokenType == tt.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)>float(right)
        elif expr.operator.tokenType == tt.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)>=float(right)
        elif expr.operator.tokenType == tt.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)<float(right)
        elif expr.operator.tokenType == tt.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left)<=float(right)
        elif expr.operator.tokenType == tt.BANG_EQUAL:
            return left!=right
        elif expr.operator.tokenType == tt.EQUAL_EQUAL:
            return left==right
        return None

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.tokenType == tt.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return float(right)*-1.0
        if expr.operator.tokenType == tt.BANG:
            return not self.truthy(right)

        return None

    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")


    def truthy(self, object):
        if isinstance(object, bool):
            return object
        if object is None:
            return False
        return True


    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visitVarStmt(self, stmt):
        value=None
        if stmt.initializer is not None:
            value=self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)

    def visitAssignExpr(self, expr):
        value=self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value