from typing import *
import operator

def evaluate_args(func: Callable) -> Callable:
    return lambda *args: func(*[arg() for arg in args])

def if_(cond: Callable[[], bool], arg1: Callable, arg2: Callable) -> Any:
    if cond():
        return arg1()
    return arg2()

def define_(signature: str, body):
    from objects import Function

    signature = signature[1:-1].split(" ")
    name = signature.pop(0)
    parameters = signature

    function = Function(
        name,
        parameters,
        body
    )
    return function

functions = {
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
    "define": define_
}

""" 
TODO:
    - let 
    - lambda
    - list
    - cond
    - https://groups.csail.mit.edu/mac/ftpdir/scheme-7.4/doc-html/scheme_2.html
"""

variables = {
    "PI": 3.14
}