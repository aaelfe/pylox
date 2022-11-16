from expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from tokenType import TokenType
from myToken import myToken

class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs):
        result="("+name
        for expr in exprs:
            #print(expr)
            result+=" "+expr.accept(self)
        result+=")"
        return result

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        if not expr.value:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

def main():
    expression=Binary(
        Unary(
            myToken(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        myToken(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )
    print(AstPrinter().print(expression))

if __name__=="__main__":
    main()