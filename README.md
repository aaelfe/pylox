# pylox

Built with guidance from Crafting Interpreters by Robert Nystrom.

Lox interpreter written in Python. Project is nearly complete, but there are issues involved with reassignment within nested scopes. So, currently for loops and many other instances of variable reassignment don't work.

## Running the Interpreter

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
