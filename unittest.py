from interpreter import interpret_expression, interpret_module

def add_test():
    code = "(+ 2 3)"
    assert interpret_expression(code) == 5
    
def division_test():
    code = "(/ 6 2)"
    assert interpret_expression(code) == 3
    
def nested_arithmetic_test():
    code = "(/ 6 (+ 1 1))"
    assert interpret_expression(code) == 3

def deeply_nested_arithmetic_test():
    code = "(/ (* 1 12) (/ 6 (- 3 1)))"
    assert interpret_expression(code) == 4

def if_negative_test():
    code = "(if (<= 3 2)\n\t(+ 4 5)\n\t(* 2 3))"
    assert interpret_expression(code) == 6

def if_positive_test():
    code = "(if (> 3 2)\n\t(+ 4 5)\n\t(* 2 3))"
    assert interpret_expression(code) == 9

def function_test():
    code = "(define (add1 n) (+ n 1))\n(add1 2)\n(add1 4)"
    assert interpret_module(code) == "3\n5"

def fibonacci_test():
    code = "(define (fib n)\n\t(if (<= n 2)\n\t\t1\n\t\t(+ (fib (- n 1)) (fib (- n 2)))))\n(fib 6)\n(fib 20)"
    assert interpret_module(code) == "8\n6765"
    

def run_all_tests():
    print('Running tests...')
    
    add_test()
    division_test()
    nested_arithmetic_test()
    deeply_nested_arithmetic_test()
    if_negative_test()
    if_positive_test()
    function_test()
    fibonacci_test()
    
    print("Passed tests! :)")

if __name__ == "__main__":
    run_all_tests()
