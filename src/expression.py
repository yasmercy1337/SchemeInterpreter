from __future__ import annotations
from code_parser import *
from scope import Scope
from typing import *

class Expression:
    
    def __init__(self, code: str, scope: Scope = None):
        self.code: str = code
        self.scope: Scope = scope
        self.parsed: bool = False
        
        self.operator: Callable = None
        self.arguments: list[Expression] = None
        self.value: Any = "UNSET"
    
    def parse(self):
        code = parse_whitespace(self.code)
        self.parsed = True
        if is_function(code): # function call
            code = strip_parens(code)
            operator, *arguments = group_blocks(code)
            if is_function(operator):
                self.operator = Expression(operator, self.scope)()
            else:
                self.operator = self.scope.get(operator)
            if not self.operator:
                raise NameError(f"'{operator}' is not defined")
            self.arguments = [Expression(arg, self.scope) for arg in arguments]
            return
        try:
            operand = group_blocks(code)[0]
            if value := self.scope.get(operand):
                self.value = value
                return
            self.value = parse_word(group_blocks(code)[0])
        except ValueError:
            raise NameError(f"'{code}' can not be parsed")
            
    def __call__(self) -> Any:
        if not self.parsed:
            self.parse()
        if not self.value == "UNSET":
            return self.value
        return self.operator(*self.arguments)
    
    def __repr__(self) -> str:
        if not self.value == "UNSET":
            return f"value='{self.value}'"
        if self.operator is not None and self.arguments is not None:
            return f"operator='{self.operator}' args={self.arguments}"
        return self.code

def is_function(code: str) -> bool:
    return code[0] == "(" and code[-1] == ")"