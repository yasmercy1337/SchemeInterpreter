from interpreter import *


def main():
    
    with open("code.txt", "r") as f:
        code = "".join(f.readlines())
        print(f"Interpreting: \n{code}\n")
        # output = interpret_expression(code)
        output = interpret_module(code)
        print(output)
    

if __name__ == "__main__":
    main()