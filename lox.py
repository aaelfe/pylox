import sys
import scanner
# from tokenType import TokenType
# from myToken import myToken
# from parser import Parser
# from astPrinter import AstPrinter
import tokenType
import myToken
import parser as p
import astPrinter
import interpreter as interp

args=sys.argv
argCount=len(sys.argv) #number of args

class Lox:
    def __init__(self):
        self.hadError=False
        self.hadRuntimeError=False
        self.interpreter=interp.Interpreter()

    def runFile(self, path):
        file=open(path, "r")
        input=file.read()
        file.close()
        self.run(input)
        if(self.hadError):
            sys.exit(65)
        if(self.hadRuntimeError):
            sys.exit(70)

    def runPrompt(self):
        while 1:
            line=input("> ")
            if line=="quit":
                break
            self.run(line)
            print()
            self.hadError=False

    def run(self, source):
        localScanner=scanner.Scanner(source)
        tokens=list(localScanner.scanTokens())
        # for token in tokens:
        #     print(token.tokenType, end=" | ")
        # print()
        parser = p.Parser(tokens)
        statements=parser.parse()

        if self.hadError:
            return
        # print(expression)
        # print(astPrinter.AstPrinter().print(expression))
        self.interpreter.interpret(statements)
    
    def error(self, line, message):
        self.report(line, "", message)
    
    def report(self, line, where, message):
        print("[line "+str(line)+"] Error"+where+": "+message)
        self.hadError=True

    def parseError(self, token, message):
        if token.tokenType == tokenType.TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def runtimeError(self, error):
        print(str(error)+"\n[line "+error.token.line+" ]")
        self.hadRuntimeError=True

#create instance of the interpreter to use in main below
interpreter = Lox()
if __name__ == "__main__":
    if argCount>2:
        print("Usage: pylox [script]") #incorrect usage
        sys.exit(64)
    elif argCount==2:
        interpreter.runFile(args[1]) #run file
    else:
        interpreter.runPrompt() #Read Evaluate Print Loop (REPL)
    