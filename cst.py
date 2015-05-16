class CST:
    def __init__(self, token):
        self.token = token
        self.children = []

def print_cst(cst, tabs):
    parent_indent = "  " * (tabs - 1)
    child_indent = "  " * tabs
    print("%s%s" % (parent_indent, cst.token["type"]))
    for i in cst.children:
        if i.children is not []:
            print_cst(i, tabs+1)

def generate_cst(token_list):
    cst = CST({"type": "Program"})
    (result, token_list) = parse_block(token_list)
    cst.children += [result, CST(token_list.pop(0))]
    return cst

def parse_block(token_list):
    cst = CST({"type": "Block"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_statement_list(token_list)
    if result is not None:
        cst.children += [result]
    cst.children += [CST(rest.pop(0))]
    return (cst, rest)

def parse_statement_list(token_list):
    # Assignment statement not consuming tokens correctly. Line 9 of test file.
    cst = CST({"type": "Statement List"})
    if token_list[0]["type"] is "CloseBrace":
        return (None, token_list)
    (result, token_list) = parse_statement(token_list)
    cst.children += [result]
    (result, token_list) = parse_statement_list(token_list)
    if result is not None:
        cst.children += [result]
    return (cst, token_list)

def parse_statement(token_list):
    cst = CST({"type": "Statement"})
    result = None
    rest = None
    if token_list[0]["type"] is "Print":
        (result, rest) = parse_print_statement(token_list)
    elif token_list[0]["type"] is "Id":
        (result, rest) = parse_assign_statement(token_list)
    elif token_list[0]["type"] is "IdType":
        (result, rest) = parse_var_decl(token_list)
    elif token_list[0]["type"] is "While":
        (result, rest) = parse_while_statement(token_list)
    elif token_list[0]["type"] is "If":
        (result, rest) = parse_if_statement(token_list)
    elif token_list[0]["type"] is "OpenBrace":
        (result, rest) = parse_block(token_list)

    cst.children += [result]
    return (cst, rest)

def parse_print_statement(token_list):
    cst = CST({"type": "Print Statement"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    (result, rest) = parse_expr(token_list)
    cst.children += [result, CST(rest.pop(0))]
    return (cst, rest)

def parse_assign_statement(token_list):
    cst = CST({"type": "Assignment Statement"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    (result, token_list) = parse_expr(token_list)
    cst.children += [result]
    return (cst, token_list)

def parse_var_decl(token_list):
    cst = CST({"type": "Variable Declaration"})
    cst.children += [CST(token_list.pop(0)), CST(token_list.pop(0))]
    return (cst, token_list)

def parse_while_statement(token_list):
    cst = CST({"type": "While Statement"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_bool_expr(token_list)
    cst.children += [result]
    (result, rest) = parse_block(rest)
    cst.children += [result]
    return (cst, rest)

def parse_if_statement(token_list):
    cst = CST({"type": "If Statement"})
    cst.children += [CST(token_list.pop(0))]
    (result, rest) = parse_bool_expr(token_list)
    cst.children += [result]
    (result, rest) = parse_block(rest)
    cst.children += [result]
    return (cst, rest)

def parse_expr(token_list):
    # REPLACED REST WITH TOKEN_LIST
    # I DON'T EVEN KNOW
    cst = CST({"type": "Expression"})
    result = None
    if token_list[0]["type"] is "Digit":
        (result, token_list) = parse_int_expr(token_list)
    elif token_list[0]["type"] is "CharList":
        (result, token_list) = parse_string_expr(token_list)
    elif token_list[0]["type"] in ["OpenParen", "BoolVal"]:
        (result, token_list) = parse_bool_expr(token_list)
    elif token_list[0]["type"] is "Id":
        result = CST(token_list.pop(0))
    cst.children += [result]
    return (cst, token_list)

def parse_int_expr(token_list):
    cst = CST({"type": "Int Expression"})
    cst.children += [CST(token_list.pop(0))]
    if token_list[0]["type"] is "IntOp":
        cst.children += [CST(token_list.pop(0))]
        (result, rest) = parse_expr(token_list)
        cst.children += [result]
        return (cst, rest)
    return (cst, token_list)

def parse_string_expr(token_list):
    cst = CST({"type": "String Expression"})
    cst.children += [CST(token_list.pop(0))]
    return (cst, token_list)

def parse_bool_expr(token_list):
    cst = CST({"type": "Boolean Expression"})
    rest = token_list
    if rest[0]["type"] is "OpenParen":
        cst.children += [CST(rest.pop(0))]
        (result, rest) = parse_expr(rest)
        cst.children += [result, CST(rest.pop(0))]
        (result, rest) = parse_expr(rest)
        cst.children += [result, CST(rest.pop(0))]
        return (cst, rest)
    else:
        cst.children += [CST(rest.pop(0))]
        return (cst, rest)
