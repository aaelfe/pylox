from lox import Lox
import sys
from io import StringIO

stdout_fileno = sys.stdout

loopsOutput = """1
2
3
4
1
2
3
4
"""

scopeOutput = """inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c
"""

ifElseOutput = """Variable a equals y
Variable a doesn't equal z
Variable a equals x
"""

expressionsOutput = """39
false
true
"""

testOutput = """Not three strikes.
x
Not three strikes.
xx
Three strikes!
xxx
Not three strikes.
xxxx
"""

#This test runs examples/loops.lox through the interpreter
#Passes if the stdout equals the content of the loopsOutput variable
def test_loops():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/loops.lox')
    assert myOutput.getvalue() == loopsOutput

#This test runs examples/scope.lox through the interpreter
#Passes if the stdout equals the content of the scopeOutput variable
def test_scope():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/scope.lox')
    assert myOutput.getvalue() == scopeOutput

#This test runs examples/ifElse.lox through the interpreter
#Passes if the stdout equals the content of the ifElseOutput variable
def test_if_else():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/ifElse.lox')
    assert myOutput.getvalue() == ifElseOutput

#This test runs examples/expressions.lox through the interpreter
#Passes if the stdout equals the content of the expressionsOutput variable
def test_expressions():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/expressions.lox')
    assert myOutput.getvalue() == expressionsOutput

#This test runs examples/test.lox through the interpreter
#Passes if the stdout equals the content of the testOutput variable
def test_test():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/test.lox')
    assert myOutput.getvalue() == testOutput

sys.stdout = stdout_fileno