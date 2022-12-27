from __future__ import annotations
from expression import Expression
from functions import Function
from functools import wraps
from code_parser import *
from conslist import *
from typing import *
import operator

def evaluate_args(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args):
        return func(*[arg() for arg in args])
    return wrapper

def if_(cond: Expression, then_block: Expression, else_block: Expression) -> Any:
    if cond():
        return then_block()
    return else_block()

def cond_(*conds: Expression) -> Any:
    for condition in conds:
        predicate, *actions = group_blocks(strip_parens(condition.code))
        if predicate == "else" or Expression(predicate, condition.scope)():
            # conditions can do all the actions, but only return the last
            results = [Expression(action, condition.scope)() for action in actions]
            return results[-1]
    raise ValueError

@evaluate_args    
def display_(arg: Any) -> None:
    print(arg, end="")

def newline_() -> None:
    print()
    
@evaluate_args
def begin_(*args: Any) -> None:
    return args[-1]

def let_(variables: Expression, operation: Expression) -> Any:
    variables = group_blocks(strip_parens(variables.code))
    for variable in variables:
        name, value = group_blocks(strip_parens(variable))
        value = Expression(value, operation.scope)()
        operation.scope.add(name, value)
    return operation()
    
def define_(signature: Expression, body: Expression, scope) -> tuple[str, Any]:
    from scope import Scope
    
    # function
    if signature.code[0] == "(" and signature.code[-1] == ")":
        signature = group_blocks(strip_parens(signature.code))
        name, *params = signature
        function = Function(name, params, body.code, Scope(scope))
        scope.add(name, function)
        return name, function
    # assignment
    name = signature.code.split(" ")[0]
    return name, body()

@evaluate_args
def list_(*args: Any) -> ConsList:
    return ConsList.from_list(list(args))

@evaluate_args
def cons_(head: Any, next: Any) -> ConsList:
    return ConsList(head, next)

@evaluate_args
def append_(*args: ConsList) -> ConsList:
    if not args:
        return ConsList()
    head, *next = args
    for arr in next:
        head.append(arr)
    return head

@evaluate_args
def car_(arr: ConsList) -> Any:
    return arr.head

@evaluate_args
def cdr_(arr: ConsList) -> Any:
    return arr.next

@evaluate_args
def null_(arr: ConsList) -> Any:
    return arr is None or (arr.head is None and arr.next is None)

def lambda_(params: Expression, body: Expression) -> Function:
    params = strip_parens(params.code).split(" ")
    return Function("lambda", params, body.code, body.scope)

operators: dict[str, Callable] = {
    # inconsistency: arithmetic operations can take in multiple in scheme
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
    "or": evaluate_args(operator.or_),
    "and": evaluate_args(operator.and_),
    "eq?": evaluate_args(operator.is_),
    "display": display_,
    "newline": newline_,
    "begin": begin_,
    
    # special form
    "if": if_,
    "define": define_,
    "cond": cond_,
    "let": let_,
    "lambda": lambda_,
    
    # list operations
    "list": list_,
    "cons": cons_,
    "append": append_,
    "car": car_,
    "cdr": cdr_,
    "null?": null_,
    
}

variables: dict[str, Any] = {
    "PI": 3.14
}