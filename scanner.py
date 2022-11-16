from tokenType import TokenType
from myToken import myToken
import lox

class Scanner:
    def __init__(self, source):
        self.source=source
        self.tokens=[]
        self.start=0
        self.current=0
        self.line=1
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }
    
    def scanTokens(self):
        while not self.isAtEnd():
            self.start=self.current
            self.scanToken()
        self.tokens.append(myToken(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        character=self.advance()
        match character:
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)
            case "!":
                self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
            case "<":
                self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">":
                self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek()!="\n" and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case "\n":
                self.line=self.line+1
            case '"':
                self.string()
            case _:
                if character.isdigit():
                    self.number()
                elif character.isalpha() or character=="_":
                    self.identifier()
                elif not character==" " and not character=="\r" and not character=="\t":
                    l=lox.Lox()
                    l.error(self.line, "Unexpected character.")
    
    def identifier(self):
        while self.peek().isalpha() or self.peek().isdigit():
            self.advance()
        text=self.source[self.start:self.current]
        tokenType=self.keywords.get(text)
        if tokenType is None:
            tokenType=TokenType.IDENTIFIER
        self.addToken(tokenType)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek()=="." and self.peekNext().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        while self.peek()!='"' and not self.isAtEnd():
            if self.peek()=="\n":
                self.line=self.line+1
            self.advance()
        if self.isAtEnd():
            l=lox.Lox()
            l.error(self.line, "Unterminated string.")
            return
        self.advance()
        value=self.source[self.start+1:self.current-1]
        self.addToken(TokenType.STRING, value)

    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current]!=expected:
            return False
        self.current=self.current+1
        return True

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self):
        if self.current+1>=len(self.source):
            return "\0"
        return self.source[self.current+1]
    
    def isAtEnd(self):
        return self.current>=len(self.source)

    def advance(self):
        self.current=self.current+1
        return self.source[self.current-1] #why doesn't Python have ++?

    def addToken(self, tokenType, literal=None):
        text=self.source[self.start:self.current]
        self.tokens.append(myToken(tokenType, text, literal, self.line))