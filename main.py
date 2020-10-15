import ply.lex as lex
import sys
from lex_analyzer import Lexer

lex_ = Lexer()
lex_.build_lex()
if len(sys.argv) == 1:
    print("Not file name entered")
else:
    name_file = open(sys.argv[1])
    if name_file:
        lex_.lex.input(name_file.read())
        name_file.close()
        while True:
            tok = lex_.lex.token()
            if not tok:

                break
            print(tok)
