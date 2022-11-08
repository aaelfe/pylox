class myToken:
    def __init__(self, tokenType, lexeme, literal, line):
        self.tokenType=tokenType
        self.lexeme=lexeme
        self.literal=literal
        self.line=line
    def __str__(self):
        #return f'{self.tokenType} {self.lexeme} {self.literal}'
        return self.lexeme