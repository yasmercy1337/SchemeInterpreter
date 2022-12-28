from interpreter import *
from pathlib import Path

def test():
    from unittest import test_all
    test_all()
    
def interpret_file():
    path = Path.cwd().parent / "code.txt"
    with open(str(path), "r") as f:
        code = "".join(f.readlines())
        print(f"Interpreting: \n{code}\n")
        output = interpret_module(code)
        print(output)
        
def main():
    """ DRIVER CODE """   
    #test()
    # interpret_file()
    repl()

if __name__ == "__main__":
    main()