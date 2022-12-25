from expression import Expression
from module import Module
from typing import *

def interpret_module(code: str) -> Any:
    module = Module(code)
    return module()
     

def interpret_expression(code: str) -> Any:
    module = Module(code)
    expression = Expression(code, module.scope)
    return expression()