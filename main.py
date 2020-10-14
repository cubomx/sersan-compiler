import ply.lex as lex
import sys
tokens = ('IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL')


# when finding new line /n
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# the following functions are code to do when finding some token

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    print("IDENT " + t.value)

def t_CTE_REAL(t):
    r'[1-9][0-9]*'
    print("CTE-REAL " + t.value)

def t_DELIM(t):
    r'[)(;\]\[]'
    print("DELIM " + t.value)

def t_OP_ARIT(t):
    r'[+*/%^-]'
    print("OP-ARIT " + t.value)

def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
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


