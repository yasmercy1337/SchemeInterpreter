def strip_parens(code: str) -> str:
    return code[1:-1]

def split_words(code: str, delim: str = " ") -> list[str]:
    return code.split(delim)

def group_blocks(code: str, delim: str = " ") -> list[str]:
    out = []
    count = 0
    current = ""
    
    for char in code:
        count += (char == "(") - (char == ")") + (char == "[") - (char == "]")     
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
    for check_type in numeric_types:
        try:
            code = check_type(code)
            return code
        except ValueError:
            continue
    
    # lists
    if code[0] == "[" and code[-1] == "]":
        import conslist
        arr = [parse_word(word) for word in strip_parens(code).split(" ")]
        return conslist.ConsList.from_list(arr)
    
    # booleans
    if code == "#t":
        return True
    elif code == "#f":
        return False
    
    # None
    if code == "None":
        return None
    raise ValueError(f"Unknown object '{code}'")

def parse_whitespace(code: str) -> str:
    code = clear_comments(code)
    return remove_consecutive_whitespace(code.replace("\n", " ").replace("\t", " "))

def remove_consecutive_whitespace(string: str) -> str:
    remove = False
    out = ""
    for char in string:
        if not remove or char != " ":
            out += char
        remove = char == " "
    return out

def clear_line_comment(code: str) -> str:
    try:
        return code[:code.index(";")]
    except ValueError:
        return code
        
def clear_comments(code: str) -> str:
    return "\n".join([clear_line_comment(line) for line in code.split("\n")]).strip()

def buffer_parens(code: str) -> str:
    return code.replace("(", " ( ").replace(")", " ) ")

def unbuffer_parens(code: str) -> str:
    return code.replace(" ( ", "(").replace(" ) ", ")")