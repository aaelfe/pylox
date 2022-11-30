import loxCallable as c
import loxInstance as i

class LoxClass(c.LoxCallable):
    def __init__(self, name, methods):
        self.name=name
        self.methods=methods
    def __str__(self):
        return self.name
    def call(self, interpreter, arguments):
        instance=i.LoxInstance(self)
        return instance
    def arity(self):
        return 0
    def findMethod(self, name):
        if name in self.methods:
            return self.methods[name]
        return None