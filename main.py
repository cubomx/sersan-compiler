import ply.lex as lex
import sys
tokens = ('IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL')

# the next lines are how the regular expresions should be made

'''t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_OP_ARIT = r'\[+-*/%^]'
t_CTE_REAL = r'[1-9][0-9]*'
t_DELIM = r'[();[]:]'''


# when finding new line /n
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# the following functions are code to do when finding some token

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    print("IDENT " + t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex_= lex.lex()





if len(sys.argv) == 1:
    print("Not file name entered")
else:
    name_file = open(sys.argv[1])
    if name_file:
        lex_.input(name_file.read())
        name_file.close()
        while True:
            tok = lex_.token()
            if not tok:

                break
            print(tok)


