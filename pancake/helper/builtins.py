from copy import deepcopy
from typing import Callable

from pancake.helper.function import Function
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

class Input(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        string = stack.pop()
        stack.append(input(string))

class Print(Builtin):
    def execute(self, stack, function_scope, variable_scope):
        a = stack.pop()
        print(pancake_print(a))

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
        ls = stack.pop()
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
    "print": Print(),

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
