from dataclasses import dataclass, field
from typing import *
import scheme_builtins


class Scope:
    def __init__(self):
        self.functions: dict[str, Callable] = {}
        self.variables: dict[str, Any] = {}
        self.child_scopes: list[Scope] = []
        set_builtins(self)
      
        
def set_builtins(scope: Scope) -> None:
    scope.functions.update(scheme_builtins.functions)
    scope.variables.update(scheme_builtins.variables)
    
    
@dataclass
class Function:
    name: str
    parameters: list[str]
    body: str
    scope: Scope = field(default_factory=Scope)
    
    def __call__(self, *args) -> Any:
        code = self.body  # copy
        for parameter, arg in zip(self.parameters, args):
            code = code.replace(parameter, str(arg))
        return Expression(code)(self.scope)
    
    
@dataclass
class Expression:
    code: str
    
    def __call__(self, scope: Scope = None) -> Any:
        if not self.code:
            return
        
        if not scope:
            scope = Scope()
        
        code = parse_whitespace(self.code)
        # single variable
        if len(code.split(" ")) == 1:
            return parse_word(self.code)
        
        # function
        code = code[1:-1] # removing parens
        args = replace_with_expressions(code)
        function = scope.functions[args.pop(0).code] # can raise key error
        # print(function, *args, sep="\n")
        # print()
        return function(*args)
    
    def __repr__(self) -> str:
        return f"Expression(code={self.code})"
    
@dataclass
class Module:
    scope: Scope = field(default_factory=Scope)
    expressions: list[Expression] = field(default_factory=list)
    
    def __call__(self) -> Any:
        # iterate through expressions
        # add all functions to the module scope
        # run any expressions
        expressions = []
        
        for expression in self.expressions:
            if is_function(expression.code):
                code = expression.code[8:-1] # removing the define and parens
                signature, body = replace_with_expressions(code)
                signature = signature.code[1:-1].split(" ")
                name = signature.pop(0)
                parameters = signature
                function = Function(name, parameters, body.code)
                self.scope.functions[function.name] = function
            else:
                expressions.append(expression)        
        output = [str(expression(self.scope)) for expression in expressions]
        return "\n".join(output)
    
                
def is_function(code: str) -> bool:
    return "define" in code
     
def parse_word(code: str) -> Any:
    """ Takes in an 'word' and parses it to a correct type"""

    # string
    if code[0] == '"' and code[-1] == '"':
        return code[1:-1]
    
    # int or floats
    numeric_types = [int, float]
    for type in numeric_types:
        try:
            code = type(code)
            return code
        except ValueError:
            continue
        
    # booleans
    if code == "#t":
        return True
    elif code == "#f":
        return False
    
    raise ValueError(f"Unknown object '{code}'")


def parse_whitespace(code: str) -> str:
    return remove_consecutive_whitespace(code.replace("\n", " ").replace("\t", " "))
        
        
def remove_consecutive_whitespace(string: str) -> str:
    remove = False
    out = ""
    for char in string:
        if not remove or char != " ":
            out += char
        remove = char == " "
    return out

    
def replace_with_expressions(code: str) -> list[Expression]:    
    out = []
    count = 0
    current = ""
    
    for char in code:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
        
        if char == " " and count == 0:
            out.append(Expression(current))
            current = ""
            continue
        current += char

    if current:
        out.append(Expression(current))
    return out 