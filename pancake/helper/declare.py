from enum import Enum

class DeclareType(Enum):
    VARIABLE = 0
    FUNCTION = 1

class Declare:
    def __init__(self, name, declare_type):
        self.name = name
        self.declare_type = declare_type

    def __str__(self):
        if self.declare_type == DeclareType.VARIABLE:
            return f"={self.name}"
        else:
            return f"=>{self.name}"
