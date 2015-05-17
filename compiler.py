import sys, lexer, parser, cst

def main():
    f = open(sys.argv[1], 'r')
    program = f.read()
    f.close()
    token_list = lexer.lex_program(program)
    parser.parse_program(token_list)
    cst_root = cst.CST({"type": "Program"})
    cst_root.generate_cst(token_list)
    print("Compilation successful!")

if __name__ == '__main__':
    main()
