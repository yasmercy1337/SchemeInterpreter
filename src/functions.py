from expression import Expression
from scope import Scope
from typing import *

class Function(Expression):
    
    def __init__(self, name: str, params: list[str], code: str, scope: Scope = None):
        super().__init__(code, scope)    
        self.name: str = name
        self.params: list[str] = params
    
    def __call__(self, *args) -> Any:
        code = self.code
        for parameter, arg, in zip(self.params, args):
            code = code.replace(parameter, str(arg()))
        return Expression(code, self.scope)()