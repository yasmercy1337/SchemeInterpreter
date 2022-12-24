from typing import *
from objects import *


def interpret_module(code: str) -> Any:
    module = Module()
    code = parse_whitespace(code)
    module.expressions = replace_with_expressions(code)
    return module()
    

def interpret_expression(code: str) -> Any:
    module = Module()
    expression = Expression(code)
    return expression(module.scope)     
