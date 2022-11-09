# pylox

Lox interpreter written in Python. At this checkpoint, only the scanner is complete.

## Running the Scanner

The interpreter has two modes.

1. Real Evaluate Print Loop (REPL)
    - Usage: `py lox.py`
    - Enter Lox code and each token will be printed with `|` between each
    - Enter quit to end the program
2. Run a file
    - Usage: `py lox.py \<filename\>`
    - File will be scanned and each token will be printed with with `|` between each

## Running Tests

- To run tests, use `python -m pytest tests/ -vv`
