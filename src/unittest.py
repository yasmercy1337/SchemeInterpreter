from interpreter import interpret_expression, interpret_module

def add_test():
    code = "(+ 3 2)"
    assert interpret_expression(code) == 5
    
def division_test():
    code = "(/ 6 2)"
    assert interpret_expression(code) == 3
    
def nested_arithmetic_test():
    code = "(/ 6 (+ 1 1))"
    assert interpret_expression(code) == 3

def if_negative_test():
    code = "(if (<= 3 2)\n\t(+ 4 5)\n\t(* 2 3))"
    assert interpret_expression(code) == 6
    
def if_positive_test():
    code = "(if (> 3 2)\n\t(+ 4 5)\n\t(* 2 3))"
    assert interpret_expression(code) == 9
    
def function_test():
    code = "(define (add1 n) (+ n 1))\n(add1 2)\n(add1 4)"
    assert interpret_module(code) == "3\n5"
    
def factorial_test():
    code = "(define (fact-iter current n)\n\t(if (= n 1)\n\t\tcurrent\n\t\t(fact-iter (* current n) (- n 1))))\n(fact-iter 1 5)"
    assert interpret_module(code) == "120"
    
def fibonacci_test():
    code = "(define (fib n)\n\t(if (<= n 2)\n\t\t1\n\t\t(+ (fib (- n 1)) (fib (- n 2)))))\n(fib 6)\n(fib 20)"
    assert interpret_module(code) == "8\n6765"
    
def cond_test():
    code = "(cond ((> 1 3)\n               1)\n      ((> 2 3)\n       2)\n   ((> 4 3)\n       (+ 4 2))\n     (else\n          4))"
    assert interpret_expression(code) == 6
    
def let_test():
    code = "(let ((a 10)\n\t (b 20))\n\t(+ a b))"
    assert interpret_expression(code) == 30

def list_test():
    code = "(caddr (append (list 10 15) (list 8) (list 6 10 14)))"
    assert interpret_expression(code) == 8
    
def test_all():
    tests = [
        add_test, 
        division_test,
        nested_arithmetic_test,
        if_negative_test,
        if_positive_test,
        function_test,
        factorial_test,
        fibonacci_test,
        cond_test,
        let_test,
        list_test
    ]
    
    print(f"Testing {len(tests)} tests...")
    
    for test in tests:
        try:
            test()
        except AssertionError:
            print(f"Wrong output on {test} :(")
            return
        except Exception as e:
            print(f"Failed {test},", e)
            return
    
    print("Passed tests :)")
    
if __name__ == "__main__":
    test_all()