from __future__ import annotations
from code_parser import *
from scope import Scope
from typing import *

class Expression:
    
    def __init__(self, code: str, scope: Scope = None):
        self.code: str = code
        self.scope: Scope = scope
        self.operator: Callable
        self.arguments: list[Expression]
        self.value: Any = None
        self.parsed: bool = False
    
    def parse(self) -> Self:
        expressions = group_blocks(strip_parens(parse_whitespace(self.code)))
        if len(expressions) == 1:
            self.value = parse_word(expressions[0])
        else:
            self.operator = self.scope.get_function(operator := expressions.pop(0))
            self.arguments = [Expression(arg, self.scope) for arg in expressions]
            if not self.operator:
                raise NameError(f"'{operator}' is not defined")
        self.parsed = True
        return self
            
    def __call__(self) -> Any:
        if not self.parsed:
            self.parse()
            
        if self.value is not None:
            return self.value
        return self.operator(*self.arguments)
    
    def __repr__(self) -> str:
        if self.value is not None:
            return f"value='{self.value}'"
        return f"operator='{self.operator}' args={self.arguments}"
