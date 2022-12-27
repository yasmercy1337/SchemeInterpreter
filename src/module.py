from expression import Expression
from scope import Scope
from typing import *
import code_parser

class Module:
    def __init__(self, code: str):
        self.scope: Scope = Scope()
        self.expressions: list[Expression]
        self.set_builtins()
        
        code = code_parser.parse_whitespace(code)
        blocks = code_parser.group_blocks(code)
        
        # setting scope
        for function in [Expression(block, Scope(self.scope)) for block in blocks if is_function(block)]:
            self.scope.add(*function())
        self.expressions = [Expression(block, Scope(self.scope)) for block in blocks if not is_function(block)]
        
    def __call__(self) -> str:
        return "\n".join(str(expression()) for expression in self.expressions)
    
    def set_builtins(self) -> None:
        from scheme_builtins import operators, variables
        
        scope = Scope(False)
        scope.variables.update(variables)
        scope.variables.update(operators)
        self.scope = scope
        
        define = lambda signature, body: operators["define"](signature, body, self.scope)
        self.scope.variables["define"] = define
        

def is_function(expression: Expression) -> bool:
    return "define" in expression

