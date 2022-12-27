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
        self.value: Any = None
    
    def parse(self) -> Self:
        expressions = group_blocks(strip_parens(parse_whitespace(self.code)))
        self.parsed = True
        
        if len(expressions) == 1:
            if (value := self.scope.get_variable(expressions[0])):
                self.value = value
                return self
            try:
                self.value = parse_word(expressions[0])
                return self
            except ValueError:
                pass
        
        self.operator = self.scope.get_function(operator := expressions.pop(0))
        self.arguments = [Expression(arg, self.scope) for arg in expressions]
        if not self.operator:
            raise NameError(f"'{operator}' is not defined")
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
        if self.operator is not None and self.arguments is not None:
            return f"operator='{self.operator}' args={self.arguments}"
        return self.code
