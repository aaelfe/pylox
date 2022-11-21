from lox import Lox
import sys
from io import StringIO

stdout_fileno = sys.stdout

#This test executes the run function in lox.py with sample Lox code from the file test.lox
#Passes if tokens printed by scanner match the result stored in the testdotlox variable
def test_run_testdotlox():
    sys.stdout = myOutput = StringIO()
    interpreter = Lox()
    interpreter.runFile('examples/loops.lox')
    assert myOutput.getvalue() == "yo"
    
sys.stdout = stdout_fileno