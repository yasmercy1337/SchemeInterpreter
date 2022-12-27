from __future__ import annotations
from typing import *
import functools

class Scope:
    
    def __init__(self, parent_scope: Scope = None):
        self.functions: dict[str, Callable] = {}
        self.variables: dict[str, Any] = {}
        self.parent_scope = parent_scope
    
    def get_function(self, name: str) -> Callable:
        if self.functions.get(name) is not None:
            return self.functions[name]
        if self.parent_scope:
            return self.parent_scope.get_function(name)
        
        if name[0] == "c" and name[-1] == "r":
            _, *operations, _ = name
            operations = [self.get(f"c{op}r") for op in operations]
            return compose(*operations)
        
        return False
    
    def get_variable(self, name: str) -> Callable:
        if self.variables.get(name) is not None:
            return self.variables[name]
        if self.parent_scope:
            return self.parent_scope.get_variable(name)
        return False
    
    def get(self, name: str) -> Any:
        if (func := self.get_function(name)):
            return func
        return self.get_variable(name)
    
    def add_function(self, function) -> None:
        self.functions[function.name] = function
    
    def add_variable(self, name: str, value: Any) -> None:
        self.variables[name] = value
        
    def __repr__(self) -> str:
        return f"Scope(functions={list(self.functions.keys())}, variables={list(self.variables.keys())})"

def compose(*functions: Callable) -> Callable:
    import expression
    
    def _compose(f: Callable, g: Callable) -> Callable:
        return lambda x: f(lambda: g(x))
    return functools.reduce(_compose, functions)
        