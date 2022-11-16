

class Stmt():
    def accept(self, visitor):
        pass

class Visitor(Stmt):
    def visitExpressionStmt(self, stmt):
        pass
    def visitIfStmt(self, stmt):
        pass
    def visitPrintStmt(self, stmt):
        pass
    def visitVarStmt(self, stmt):
        pass
    def visitBlockStmt(self, stmt):
        pass

class Expression(Stmt):
    def __init__(self, expression):
        self.expression=expression
    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

class If(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition=condition
        self.thenBranch=thenBranch
        self.elseBranch=elseBranch
    def accept(self, visitor):
        return visitor.visitIfStmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression=expression
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)

class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
    def accept(self, visitor):
        return visitor.visitVarStmt(self)

class Block(Stmt):
    def __init__(self, statements):
        self.statements=statements
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)