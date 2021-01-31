import sys
from pprint import pprint

from pancake.interpreter.interpreter import Interpreter

if __name__ == "__main__":
    file_name = sys.argv[1]

    with open(file_name) as f:
        Interpreter.interpret(f.read())
