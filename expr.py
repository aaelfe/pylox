from myToken import myToken

class Expr():
    def accept(self, visitor):
        pass

class Visitor(Expr):
    def visitBinaryExpr(self, binary):
        pass
    def visitGroupingExpr(self, grouping):
        pass
    def visitLiteralExpr(self, literal):
        pass
    def visitUnaryExpr(self, unary):
        pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: myToken, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression
    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)

class Unary(Expr):
    def __init__(self, operator: myToken, right: Expr):
        self.operator = operator
        self.right = right
    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)