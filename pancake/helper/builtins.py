from copy import deepcopy
from typing import Callable

import pancake.interpreter.interpreter as interpreter
import pancake.interpreter.eval as evaluate
from pancake.helper.function import Function
from pancake.helper.pancake_error import PancakeError
from pancake.helper.symbol import Symbol
from pancake.helper.variable import Variable
from pancake.interpreter.print import pancake_print

class Builtin(Function):
    def __init__(self):
        super().__init__(args=[], body=[], parent_id=-1)

# GENERAL BUILTINS

class Execute(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        # Fix scoping inside nested functions, can change variables in
        # outer scope
        func = stack.pop()
        func.execute(stack, function_scope, variable_scope)
        self.scope_updates = func.scope_updates

class If(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        predicate = stack.pop()
        true = stack.pop()
        false = stack.pop()

        if predicate:
            true.execute(stack, function_scope, variable_scope)
            self.scope_updates = true.scope_updates
        else:
            false.execute(stack, function_scope, variable_scope)
            self.scope_updates = false.scope_updates

class Import(Builtin):
    def __init__(self):
        super().__init__()

    def execute(self, stack, function_scope, variable_scope):
        file_name = stack.pop()

        with open(file_name) as f:
            new_fscope = {}
            new_vscope = {}

            forms = interpreter.Interpreter.READ(f.read())
            evaluate.evaluate(forms, [], new_fscope, new_vscope)

            function_scope |= new_fscope

            for vname in new_vscope:
                self.scope_updates[vname] = new_vscope[vname]
                
            variable_scope |= new_vscope

class Input(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        string = stack.pop()
        stack.append(input(string))

class Print(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        a = stack.pop()
        print(pancake_print(a))

class Stack(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        print([str(x) for x in stack])

class Require(Builtin):
    @staticmethod
    def imports_for_function(body, fscope, vscope, already_imported) -> tuple[list, list]:
        function_imports = set()
        variable_imports = set()

        for form in body:
            if isinstance(form, Variable) and form.name not in already_imported:
                if form.name in fscope.keys():
                    function_imports.add(form.name)
                    already_imported.append(form.name)

                    inner_fimports, inner_vimports = Require.imports_for_function(fscope[form.name].body, fscope, vscope, already_imported)
                    function_imports |= inner_fimports
                    variable_imports |= inner_vimports
                elif form.name in vscope.keys():
                    variable_imports.add(form.name)
                    already_imported.append(form.name)
            elif isinstance(form, Function):
                inner_fimports, inner_vimports = Require.imports_for_function(form.body, fscope, vscope, already_imported)
                function_imports |= inner_fimports
                variable_imports |= inner_vimports

        return function_imports, variable_imports

    def execute(self, stack, function_scope, variable_scope):  
        file_name = stack.pop()
        require_names = []

        for item in stack.pop():
            if not isinstance(item, Symbol):
                raise TypeError("Only symbols can be used for require!")

            require_names.append(item)

        with open(file_name) as f:
            new_fscope = {}
            new_vscope = {}

            forms = interpreter.Interpreter.READ(f.read())
            evaluate.evaluate(forms, [], new_fscope, new_vscope)

            for fname in new_fscope.keys():
                if fname in require_names:
                    fimports, vimports = Require.imports_for_function(new_fscope[fname].body, new_fscope, new_vscope, [])
                    
                    for fimport in fimports:
                        function_scope[fimport] = new_fscope[fimport]

                    for vimport in vimports:
                        variable_scope[vimport] = new_vscope[vimport]

                    function_scope[fname] = new_fscope[fname]
                
            for vname in new_vscope.keys():
                if vname in require_names and isinstance(new_vscope[vname], Function):
                    fimports, vimports = Require.imports_for_function(new_vscope[vname].body, new_fscope, new_vscope, [])
                        
                    for fimport in fimports:
                        function_scope[fimport] = new_fscope[fimport]

                    for vimport in vimports:
                        variable_scope[vimport] = new_vscope[vimport]
                        self.scope_updates[vimport] = new_vscope[vimport]

                variable_scope[vname] = new_vscope[vname]
                self.scope_updates[vname] = new_vscope[vname]

class Throw(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        message = stack.pop()
        raise PancakeError(message)

class Try(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        try_clause = stack.pop()
        except_clause = stack.pop()

        try:
            try_clause.execute(stack, function_scope, variable_scope)
        except:
            except_clause.execute(stack, function_scope, variable_scope)

# LOGIC

class And(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        a = stack.pop()
        b = stack.pop()

        stack.append(a and b)

class Not(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        a = stack.pop()
        stack.append(not a)

class Or(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        a = stack.pop()
        b = stack.pop()

        stack.append(a or b)

# MATHS STUFF (same order as arithmetic operators, 5 2 - => 3)

class Divide(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a / b)

class Equals(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a == b)

class GreaterThan(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a > b)

class GreaterThanEqual(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a >= b)

class LessThan(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a < b)

class LessThanEqual(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a <= b)

class Minus(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a - b)

class Mod(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a % b)

class Multiply(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a * b)

class Plus(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        b = stack.pop()
        a = stack.pop()

        stack.append(a + b)

# LIST STUFF

class Append(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        ls = deepcopy(stack.pop())
        element = stack.pop()

        ls.append(element)
        stack.append(ls)

class Length(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        ls = stack.pop()

        stack.append(len(ls))

class Nth(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        ls = stack.pop()
        n = stack.pop()

        stack.append(ls[n])

FUNCTION_BUILTINS = {
    "execute": Execute(),
    "if": If(),
    "import": Import(),
    "print": Print(),
    "require": Require(),
    "stack": Stack(),
    "throw": Throw(),
    "try": Try(),

    "and": And(),
    "not": Not(),
    "or": Or(),

    "+": Plus(),
    "-": Minus(),
    "*": Multiply(),
    "/": Divide(),
    "<": LessThan(),
    "<=": LessThanEqual(),
    ">": GreaterThan(),
    ">=": GreaterThanEqual(),
    "eq": Equals(),
    "mod": Mod(),

    "append": Append(),
    "length": Length(),
    "nth": Nth()
}
