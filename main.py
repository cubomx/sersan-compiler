
import sys
from lex_analyzer import Lexer
from syntax_analyzer import Syntax

lex_ = None

if len(sys.argv) == 1:
    print("Not file name entered")
else:
    # Ge the file name from the command line
    file_name = sys.argv[1]
    file_ = open(file_name)

    lex_ = Lexer(file_name.split(".")[0])
    lex_.build_lex()

    syntax = Syntax()
    syntax.build()
    # Read the source file

    result = syntax.parser.parse("variables")
    if result:
        print(result)



lex_.close_file()

