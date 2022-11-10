from lox import Lox
import sys
from io import StringIO

testdotlox = "fun | foo | ( | bar | , | bar2 | ) | { | x | = | \"hi\" | ; | return | ( | 2 | * | bar | ) | / | bar2 | ; | } |  | "
test2dotlox = "fun | funcWithArgs | ( | base | , | power | ) | { | var | result | = | base | ; | for | ( | var | a | = | 0 | ; | a | < | power | ; | a | = | a | + | 1 | ) | { | result | = | result | * | base | ; | } | return | result | ; | } | fun | main | ( | ) | { | print | \"2^3\" | ; | print | funcWithArgs | ( | 2 | , | 3 | ) | ; | print | \"10^4\" | ; | print | funcWithArgs | ( | 10 | , | 4 | ) | ; | } | main | ( | ) | ; |  | "

stdout_fileno = sys.stdout

#This test executes the run function in lox.py with sample Lox code from the file test.lox
#Passes if tokens printed by scanner match the result stored in the testdotlox variable
def test_run_testdotlox():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('test.lox')
    assert myOutput.getvalue() == testdotlox

#This test executes the run function in lox.py with sample Lox code from the file test2.lox
#Passes if tokens printed by scanner match the result stored in the test2dotlox variable
def test_run_test2dotlox():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('test2.lox')
    assert myOutput.getvalue() == test2dotlox
    
sys.stdout = stdout_fileno