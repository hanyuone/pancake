from copy import copy, deepcopy
from typing import Tuple

from pancake.helper.declare import Declare
from pancake.helper.variable import Variable

# Avoid circular imports
import pancake.interpreter.eval as evaluate

class Function:
    ID = 0
    CLOSURE_ID = 0

    # Gives a function a unique ID (needed for function scoping)
    @staticmethod
    def new_id():
        try:
            return Function.ID
        finally:
            Function.ID += 1

    # Gives a function a unique closure ID
    # (needed for currying and referencing variables inside
    # nested functions)
    @staticmethod
    def new_closure_id():
        try:
            return Function.CLOSURE_ID
        finally:
            Function.CLOSURE_ID += 1

    def __init__(self, args, body, parent_id=-1, closure=False):
        self.id = Function.new_id()

        if closure:
            self.args = args
            self.body = body
        else:
            self.args = [f"{self.id}#{arg}" for arg in args]
            self.body = Function.edited_body(self.id, args, body)

        self.parent_id = parent_id
        self.scope_updates = {}

    # Given the function's arguments and body, displays it
    # in a user-readable format
    @staticmethod
    def display(args: str, body: str) -> str:
        if len(args) == 0 and len(body) == 0:
            return "{:}"
        elif len(args) == 0:
            return f"{{: {body} }}"
        else:
            return f"{{ {args} : {body} }}"

    def __str__(self):
        cleaned_args = []

        for arg in self.args:
            cleaned_args.append(Function.clean_name(arg))

        cleaned_body = Function.clean_body(deepcopy(self.body))
        body_string = " ".join(str(x) for x in cleaned_body)

        return Function.display(" ".join(cleaned_args), body_string)

    # Displays the "raw" version of a function, which basically
    # includes all "annotated" versions of argument/variable names
    # (like 25#x or @0#x instead of just x)
    def raw(self):
        body_string = " ".join(x.raw() if isinstance(x, Function) else str(x) for x in self.body)
        return Function.display(" ".join(self.args), body_string)

    # Executes the first function on the stack, given the current
    # function/variable scope
    def execute(self, stack, function_scope, variable_scope):
        for arg in reversed(self.args):
            variable_scope[arg] = stack.pop()
        
        self.scope_updates = evaluate.evaluate(self.body, stack, function_scope, variable_scope)

    # Clean a symbol in a function, removing local variable stuff (e.g. 18#y -> y)
    @staticmethod
    def clean_name(name: str) -> str:
        split = name.split("#")

        if len(split) == 1:
            return name
        else:
            return split[1]

    # Clean an entire function body
    @staticmethod
    def clean_body(body: list) -> list:
        for index in range(len(body)):
            item = body[index]

            if isinstance(item, Variable):
                body[index].name = Function.clean_name(item.name)
            elif isinstance(item, Declare):
                body[index].name = Function.clean_name(item.name)
            elif isinstance(item, Function):
                body[index].body = Function.clean_body(item.body)

        return body

    # Add little annotations to indicate the scope of various functions,
    # needed to make example/curry.pan and example/scoping.pan work properly
    @staticmethod
    def edited_body(fid: int, args: list[str], body: list) -> list:
        for index in range(len(body)):
            item = body[index]

            if isinstance(item, Variable) and item.name in args:
                body[index].name = f"{fid}#{item.name}"
            elif isinstance(item, Declare) and not Function.is_argument(item.name):
                if item.name not in args:
                    args.append(item.name)

                body[index].name = f"{fid}#{item.name}"
            elif isinstance(item, Function):
                body[index].body = Function.edited_body(fid, args, item.body)

                # Parent IDs shouldn't be overwritten by overarching functions,
                # so we set it so that it's only writeable once
                if body[index].parent_id == -1:
                    body[index].parent_id = fid

        return body

    # Checks if the current variable name is an argument or not
    # (i.e. has a # in it)
    @staticmethod
    def is_argument(name: str) -> bool:
        return "#" in name

    # Checks if the current variable is a closure argument
    # (i.e. has an @ in it)
    @staticmethod
    def is_closure(name: str) -> bool:
        return "@" in name

    # Returns the ID of the function the variable is from
    @staticmethod
    def fid_of_name(name: str) -> int:
        if name[0] == "@":
            return -1
        else:
            return int(name.split("#")[0])

    # Makes a function a closure if necessary, changing the function's body
    # to remove any local references to arguments, returning mappings
    @staticmethod
    def closureify(function: 'Function', parent_id) -> Tuple['Function', dict[str, str]]:
        new_body = deepcopy(function.body)
        mapping = {}

        for i in range(len(new_body)):
            symbol = new_body[i]

            if isinstance(symbol, Variable) \
                and Function.is_argument(symbol.name) \
                and Function.fid_of_name(symbol.name) == parent_id:
                clean = Function.clean_name(symbol.name)
                closure_name = f"@{Function.new_closure_id()}#{clean}"

                mapping[closure_name] = symbol.name
                new_body[i].name = closure_name
            elif isinstance(symbol, Function):
                closure, closure_mapping = Function.closureify(symbol, parent_id)
                mapping |= closure_mapping
                new_body[i] = closure

        result = Function(function.args, new_body, function.parent_id, closure=True)
        return result, mapping
