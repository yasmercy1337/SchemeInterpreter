from __future__ import annotations
from expression import Expression
from functions import Function
from code_parser import *
from typing import *
import operator

def evaluate_args(func: Callable) -> Callable:
    return lambda *args: func(*[arg() for arg in args])

def if_(cond: Expression, then_block: Expression, else_block: Expression) -> Any:
    if cond():
        return then_block()
    return else_block()

def define_(signature: Expression, body: Expression, scope) -> Function:
    from scope import Scope
    
    signature = group_blocks(strip_parens(signature.code))
    name, params = signature[0], signature[1:]
    function = Function(name, params, body.code, Scope(scope))
    scope.add_function(function)
    return function

operators: dict[str, Callable] = {
    "+": evaluate_args(operator.add),
    "-": evaluate_args(operator.sub),
    "*": evaluate_args(operator.mul),
    "/": evaluate_args(operator.truediv),
    "<": evaluate_args(operator.lt),
    ">": evaluate_args(operator.gt),
    "=": evaluate_args(operator.eq),
    "<=": evaluate_args(operator.le),
    ">=": evaluate_args(operator.ge),
    "not": evaluate_args(operator.not_),
    
    "if": if_,
    "define": define_,
    # TODO: and, or, cond
}

variables: dict[str, Any] = {
    "PI": 3.14
}



