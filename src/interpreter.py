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


def repl() -> None:
    module = Module("")
    expression = ""
    parens_counter = 0
    
    while True:
        # reading input
        if not parens_counter:
            code = input(">")
        else:
            code = "\n" + input("\t" * parens_counter)
        expression += code
        
        # looping until closed parenthesis
        parens_counter += code.count("(") - code.count(")")
        if parens_counter:
            continue
        
        # evaluating and printing output
        print(module.add_expression(expression))
        expression = ""
    