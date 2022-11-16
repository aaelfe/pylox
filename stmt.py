

class Stmt():
    def accept(self, visitor):
        pass

class Visitor(Stmt):
    def visitExpressionStmt(self, stmt):
        pass
    def visitPrintStmt(self, stmt):
        pass

class Expression(Stmt):
    def __init__(self, expression):
        self.expression=expression
    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression=expression
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)