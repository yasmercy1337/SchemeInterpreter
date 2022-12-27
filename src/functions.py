from expression import Expression
from scope import Scope
from typing import *
import code_parser

class Function(Expression):
    
    def __init__(self, name: str, params: list[str], code: str, scope: Scope = None):
        super().__init__(code, scope)    
        self.name: str = name
        self.params: list[str] = params
    
    def __call__(self, *args) -> Any:
        code = code_parser.buffer_parens(self.code)
        for parameter, arg, in zip(self.params, args):
            tokens = code.split(" ")
            tokens = [token if token != parameter else str(arg()) for token in tokens]
            code = " ".join(tokens)
        code = code_parser.unbuffer_parens(code)
        return Expression(code, self.scope)()