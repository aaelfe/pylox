import runtimeError as r

class LoxInstance():
    def __init__(self, klass):
        self.klass=klass
        self.fields={}
    def __str__(self):
        return self.klass.name + " instance"
    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method=self.klass.findMethod(name.lexeme)
        if method is not None:
            return method

        raise r.RuntimeE(name, "Undefined property '"+name.lexeme+"'.")
    def sett(self, name, value):
        self.fields[name.lexeme]=value