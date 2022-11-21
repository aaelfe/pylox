# pylox

Lox interpreter written in Python. At this checkpoint, the interpreter works up to a point. Loops, conditionals, logical operators, expressions, scope, all work.

Please see test code in tests/test_checkpoint.py. These are the tests that are run in the submitted image that all pass.

## Running the Scanner

The interpreter has two modes.

1. Real Evaluate Print Loop (REPL)
    - Usage: `py lox.py`
    - Enter Lox code and it will be interpreted
    - Variables will stay in memory throughout your session
    - Enter quit to end the program
2. Run a file
    - Usage: `py lox.py \<filename\>`
    - File will be interpreted and run

## Running Tests

- To run tests, use `python -m pytest tests/ -vv`
- Note, you will need to install pytest to run tests manually
