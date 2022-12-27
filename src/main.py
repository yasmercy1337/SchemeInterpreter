from interpreter import *
from pathlib import Path

def test():
    from unittest import test_all
    test_all()
        
def main():   
    # test()
    # print()
    
    path = Path.cwd().parent / "code.txt"
    with open(str(path), "r") as f:
        code = "".join(f.readlines())
        # print(f"Interpreting: \n{code}")
        output = interpret_module(code)
        print(output)

if __name__ == "__main__":
    main()