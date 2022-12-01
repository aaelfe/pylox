import loxCallable as c
import environment
import runtimeError
import environment as e
import loxFunction as f

class LoxFunction(c.LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.declaration=declaration
        self.closure=closure
        self.isInitializer=isInitializer
    
    def call(self, interpreter, arguments):
        env=environment.Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter.executeBlock(self.declaration.body, env)
        except runtimeError.Return as r:
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return r.value

        if self.isInitializer:
            return self.closure.getAt(0, "this")

        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return "<fn "+self.declaration.name.lexeme+">"

    def bind(self, instance):
        env=e.Environment(self.closure)
        env.define("this", instance)
        return f.LoxFunction(self.declaration, env, self.isInitializer)