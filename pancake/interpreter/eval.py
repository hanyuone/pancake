from copy import copy, deepcopy

from pancake.helper.declare import Declare, DeclareType
from pancake.helper.deref import Deref
from pancake.helper.reader import Reader
from pancake.helper.variable import Variable

# Avoid circular import errors
import pancake.helper.function as function

def evaluate(forms, stack, function_scope, variable_scope, is_global=False):
    scope_updates = {}

    for form in forms:
        # Comments
        if form == None:
            continue
        elif isinstance(form, Declare):
            if form.declare_type == DeclareType.VARIABLE:
                if form.name in function_scope:
                    raise NameError(f"Cannot name {form.name} as variable when it is already a function")

                new_value = stack.pop()

                if form.name in variable_scope.keys():
                    scope_updates[form.name] = new_value

                variable_scope[form.name] = new_value
            elif form.declare_type == DeclareType.FUNCTION:
                if form.name in variable_scope.keys():
                    raise NameError(f"Cannot name {form.name} as function when it is already a variable")

                function_scope[form.name] = stack.pop()
        elif isinstance(form, Deref):
            if form.name in function_scope.keys():
                stack.append(function_scope[form.name])
            else:
                raise NameError(f"Cannot dereference {form.name}, not a function")
        elif isinstance(form, Variable):
            if form.name in variable_scope.keys():
                stack.append(variable_scope[form.name])
            # Declared variables in named functions shouldn't affect the scope
            # of variables outside it
            elif form.name in function_scope.keys():
                function_scope[form.name].execute(stack, function_scope, deepcopy(variable_scope))
                scope_updates |= function_scope[form.name].scope_updates

                for key, value in scope_updates.items():
                    if key in variable_scope.keys() or function.Function.is_closure(key):
                        variable_scope[key] = value

                function_scope[form.name].scope_updates = {}
            else:
                raise NameError(f"Undefined symbol {form.name}")
        # Making closures/currying work, may need to implement GC soon
        elif isinstance(form, function.Function):
            if is_global:
                stack.append(form)
            else:
                func, mapping = function.Function.closureify(form, form.parent_id)
                
                for key, value in mapping.items():
                    scope_updates[key] = variable_scope[value]
                
                variable_scope |= scope_updates
                stack.append(func)
        else:
            stack.append(form)

    return scope_updates
