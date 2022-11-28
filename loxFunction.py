import loxCallable as c
import environment
import runtimeError

class LoxFunction(c.LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration=declaration
        self.closure=closure
    
    def call(self, interpreter, arguments):
        env=environment.Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter.executeBlock(self.declaration.body, env)
        except runtimeError.Return as r:
            return r.value

        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return "<fn "+self.declaration.name.lexeme+">"