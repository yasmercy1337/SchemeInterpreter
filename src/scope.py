from __future__ import annotations
from typing import *

class Scope:
    
    def __init__(self, parent_scope: Scope = None):
        self.functions: dict[str, Callable] = {}
        self.variables: dict[str, Any] = {}
        self.parent_scope = parent_scope
    
    def get_function(self, func_name: str) -> Callable:
        if func_name in self.functions.keys():
            return self.functions[func_name]
        
        if self.parent_scope:
            return self.parent_scope.get_function(func_name)
        
        return False
    
    def add_function(self, function) -> None:
        self.functions[function.name] = function
        
    def __repr__(self) -> str:
        return f"Scope(functions={list(self.functions.keys())}, variables={list(self.variables.keys())})"
        