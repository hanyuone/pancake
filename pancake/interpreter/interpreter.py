from pancake.helper.builtins import FUNCTION_BUILTINS
from pancake.helper.declare import Declare, DeclareType
from pancake.helper.function import Function
from pancake.helper.reader import Reader
from pancake.helper.variable import Variable

from pancake.interpreter.read import tokenise, read_form
from pancake.interpreter.eval import evaluate

class Interpreter:
    @staticmethod
    def READ(code):
        tokens = list(filter(len, tokenise(code)))
        reader = Reader(tokens)
        forms = []

        while reader.position < len(reader.tokens):
            forms.append(read_form(reader))

        return forms

    @staticmethod
    def EVAL(forms):
        stack = []
        function_scope = FUNCTION_BUILTINS
        variable_scope = {}

        evaluate(forms, stack, function_scope, variable_scope, is_global=True)

    @staticmethod
    def interpret(code):
        Interpreter.EVAL(Interpreter.READ(code))
