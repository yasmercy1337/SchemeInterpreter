def strip_parens(code: str) -> str:
    if code[0] == "(" and code[-1] == ")":
        return code[1: -1]
    return code

def split_words(code: str, delim: str = " ") -> list[str]:
    return code.split(delim)

def group_blocks(code: str, delim: str = " ") -> list[str]:
    out = []
    count = 0
    current = ""
    
    for char in code:
        count += (char == "(") - (char == ")")      
        if char == delim and count == 0:
            out.append(current)
            current = ""
            continue
        current += char

    if current:
        out.append(current)

    return out

def parse_word(code: str) -> str | int | float | bool:
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