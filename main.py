import ply.lex as lex
import sys
from lex_analyzer import Lexer

lex_ = None

if len(sys.argv) == 1:
    print("Not file name entered")
else:
    # Ge the file name from the command line
    file_name = sys.argv[1]
    file_ = open(file_name)

    lex_ = Lexer(file_name.split(".")[0])
    lex_.build_lex()
    # Read the source file
    if file_:
        lex_.lex.input(file_.read())
        file_.close()
        while True:
            # Get the tokens
            tok = lex_.lex.token()
            if not tok:
                break

#lex_.show_lex_cmp()
lex_.close_file()
