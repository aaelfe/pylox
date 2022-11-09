import sys
import scanner

args=sys.argv
argCount=len(sys.argv) #number of args

class Lox:
    def __init__(self):
        self.hadError=False

    def runFile(self, path):
        file=open(path, "r")
        input=file.read()
        file.close()
        self.run(input)
        if(self.hadError):
            sys.exit(65)

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
        for token in tokens:
            print(token, end=" | ")
    
    def error(self, line, message):
        self.report(line, "", message)
    
    def report(self, line, where, message):
        print("[line "+line+"] Error"+where+": "+message)
        self.hadError=True

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
    