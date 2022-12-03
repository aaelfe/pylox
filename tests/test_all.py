from lox import Lox
import sys
from io import StringIO

stdout_fileno = sys.stdout

#These tests run the lox files in the examples directory through the interpreter
#Each passes if the stdout equals the content of the file's respective output variable

loopsOutput = """1
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

baconOutput = """Crunch crunch crunch!
"""

bagelOutput = """Bagel instance
"""

cakeOutput = """The German chocolate cake is delicious!
"""

devonshireOutput = """DevonshireCream
"""

doughnutOutput = """Fry until golden brown.
Pipe full of custard and coat with chocolate.
"""

friendOutput = """My name is John Cena and YOU CAN'T SEE ME!
"""

fibOutput = """0
1
1
2
3
5
8
13
21
34
55
89
144
233
377
610
987
1597
2584
4181
"""

funOutput = """Hi, Dear Reader!
"""

makeCounterOutput = """0
0
"""

persistenceOutput = """global
global
"""

def test_loops():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/loops.lox')
    assert myOutput.getvalue() == loopsOutput

def test_scope():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/scope.lox')
    assert myOutput.getvalue() == scopeOutput

def test_if_else():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/ifElse.lox')
    assert myOutput.getvalue() == ifElseOutput

def test_expressions():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/expressions.lox')
    assert myOutput.getvalue() == expressionsOutput

def test_test():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/test.lox')
    assert myOutput.getvalue() == testOutput

def test_bacon():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/bacon.lox')
    assert myOutput.getvalue() == baconOutput

def test_bagel():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/bagel.lox')
    assert myOutput.getvalue() == bagelOutput

def test_cake():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/cake.lox')
    assert myOutput.getvalue() == cakeOutput

def test_devonshire():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/devonshire.lox')
    assert myOutput.getvalue() == devonshireOutput

def test_doughnut():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/doughnut.lox')
    assert myOutput.getvalue() == doughnutOutput

def test_fib():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/fib.lox')
    assert myOutput.getvalue() == fibOutput

def test_friend():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/friend.lox')
    assert myOutput.getvalue() == friendOutput

def test_fun():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/fun.lox')
    assert myOutput.getvalue() == funOutput

def test_make_counter():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/makeCounter.lox')
    assert myOutput.getvalue() == makeCounterOutput

def test_persistence():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/persistence.lox')
    assert myOutput.getvalue() == persistenceOutput

sys.stdout = stdout_fileno