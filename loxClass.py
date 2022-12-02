import loxCallable as c
import loxInstance as i

class LoxClass(c.LoxCallable):
    def __init__(self, name, superclass, methods):
        self.superclass=superclass
        self.name=name
        self.methods=methods
    def __str__(self):
        return self.name
    def call(self, interpreter, arguments):
        instance=i.LoxInstance(self)

        initializer=self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance
    def arity(self):
        initializer=self.findMethod("init")
        if initializer is None:
            return 0
        return initializer.arity()
    def findMethod(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.findMethod(name)
        return None