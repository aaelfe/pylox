# pylox

Lox interpreter written in Python.

## Running the Interpreter

The interpreter has two modes.

1. Real Evaluate Print Loop (REPL)
    - Usage: `py lox.py`
    - Enter Lox code and each token will be printed with spaces between them
    - Enter quit to end the program
2. Run a file
    - Usage: `py lox.py \<filename\>`
    - File will be scanned and each token will be printed with a space between them

## Running Tests

- To run tests, use `python -m pytest tests/ -vv`
