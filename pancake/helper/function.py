from copy import copy, deepcopy
from typing import Tuple

from pancake.helper.variable import Variable

# Avoid circular imports
import pancake.interpreter.eval as evaluate

class Function:
    ID = 0
    CLOSURE_ID = 0

    def __init__(self, args, body, parent_id=-1, closure=False):
        self.id = Function.ID

        if closure:
            self.args = args
            self.body = body
        else:
            self.args = [f"{self.id}#{arg}" for arg in args]
            self.body = Function.edited_body(self.id, args, body)

        self.parent_id = parent_id
        self.scope_updates = {}

        Function.ID += 1

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

        Function.display(" ".join(cleaned_args), body_string)

    def raw(self):
        body_string = " ".join(x.raw() if isinstance(x, Function) else str(x) for x in self.body)
        Function.display(" ".join(self.args), body_string)

    def execute(self, stack, function_scope, variable_scope):
        for arg in self.args:
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
            elif isinstance(item, Function):
                body[index].body = Function.clean_body(item.body)

        return body

    # Added to fix scoping issues
    @staticmethod
    def edited_body(fid: int, args: list[str], body: list) -> list:
        for index in range(len(body)):
            item = body[index]

            if isinstance(item, Variable) and item.name in args:
                body[index].name = f"{fid}#{item.name}"
            elif isinstance(item, Function):
                body[index].body = Function.edited_body(fid, args, item.body)

                # Parent IDs shouldn't be overwritten by overarching functions,
                # so we set it so that it's only writeable once
                if body[index].parent_id == -1:
                    body[index].parent_id = fid

        return body

    @staticmethod
    def is_argument(name: str) -> bool:
        return "#" in name

    @staticmethod
    def name_from(name: str) -> int:
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
                and Function.name_from(symbol.name) == parent_id:
                clean = Function.clean_name(symbol.name)
                closure_name = f"@{Function.CLOSURE_ID}#{clean}"

                mapping[closure_name] = symbol.name
                new_body[i].name = closure_name
            elif isinstance(symbol, Function):
                closure, closure_mapping = Function.closureify(symbol, parent_id)
                mapping |= closure_mapping
                new_body[i] = closure

        result = Function(function.args, new_body, function.parent_id, closure=True)
        return result, mapping
