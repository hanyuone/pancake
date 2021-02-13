import re

from pancake.helper.declare import Declare, DeclareType
from pancake.helper.deref import Deref
from pancake.helper.function import Function
from pancake.helper.reader import Reader
from pancake.helper.symbol import Symbol
from pancake.helper.variable import Variable

def tokenise(code):
    regex = re.compile(r"""
    [\s,]*                   # Whitespace
    (
        [\[\]{}()|]          # Special characters
        | "(?:\\.|[^\\"])*"? # Strings
        | \#.*               # Comments
        | [^\s\[\]{}(),]*   # Every other literal
    )
    """, re.VERBOSE)

    return re.findall(regex, code)

def read_function(reader):
    arguments = []
    body = []

    # Read all arguments (i.e. all tokens before : in a function)
    while reader.peek() != ":":
        arguments.append(reader.next())

    # Skip the :
    reader.next()

    while reader.peek() != "}":
        body.append(read_form(reader))

    # Skip the closing }
    reader.next()
    return Function(arguments, body)

def read_list(reader):
    elements = []

    while reader.peek() != "]":
        elements.append(read_form(reader))

    reader.next()
    return elements

def is_float(string) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def read_form(reader):
    current = reader.next()

    # Basic data types (function, list, string, int, float)
    if current == "{":
        return read_function(reader)
    elif current == "[":
        return read_list(reader)
    elif current == "true":
        return True
    elif current == "false":
        return False
    # Symbols can't consist of just a :
    elif current[0] == ":" and len(current) >= 2:
        return Symbol(current[1:])
    elif current[0] == "\"":
        return current[1:-1]
    elif current.isnumeric():
        return int(current)
    elif is_float(current):
        return float(current)
    # Comments
    elif current[0] == "#":
        return None
    # Function/variable declaration
    elif current[0:2] == "=>":
        return Declare(current[2:], DeclareType.FUNCTION)
    elif current[0] == "=":
        return Declare(current[1:], DeclareType.VARIABLE)
    # Dereference declared function
    elif current[0] == "&":
        return Deref(current[1:])
    # Regular variables
    else:
        return Variable(current)
