import ply.lex as lex
from ply import yacc


class Lexer(object):
    tokens = (
    'IDENT', 'OP_ARIT', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES', 'OP_REL', 'CTE_ENTERA', 'COMMENT', 'CTE_REAL_NON_NUM',
    'CTE_REAL_ENDING_BAD', 'CTE_ENTERA_NON_NUM', 'VARIABLES', 'CONSTANTES', 'OP_ASIG', 'TIPO','PAREN_EMPIEZA', 'PAREN_TERMINA', 'CORCHETE_EMPIEZA',
    'CORCHETE_TERMINA', 'PUNTOS_DOBLES', 'PUNTO_COMA', 'PUNTO', 'COMA', 'FIN', 'DE', 'PROGRAMA', 'FUNCION', 'PROCEDIMIENTO', 'INICIO', 'LIMPIA',
    'SI', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'REGRESA', 'IMPRIME', 'IMPRIMENL', 'LEE', 'INTERRUMPE', 'CONTINUA', 'HACER', 'SINO', 'EL',
    'VALOR', 'DE', 'QUE', 'SE', 'CUMPLA', 'SEA', 'OTRO', 'Y', 'O', 'NO')
    lexemas = dict()

    def __init__(self, filename):
        self.file_name = filename
        open(self.file_name + ".lex", 'w').close()
        open(self.file_name + ".err", 'w').close()
        self.output_file = open(self.file_name + ".lex", "a")
        self.err_file = open(self.file_name + ".err", "a")

    # when finding new line /n
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # the following functions are code to do when finding some token

    def t_COMMENT(self, t):
        r'//[.]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "COMENTARIO"
            self.add_lex("COMENTARIO", t.value)

    def t_CTE_ALFA(self, t):
        r'"[a-zA-Z0-9_ \[\]\)\(<:\¿\?,\$\#\'\?\!\¡/=*+-\^{}%°\|]*"'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-ALFA"
            self.add_lex("CTE-ALFA", t.value)

    def t_TIPO(self, t):
        r'[a|A]lfabetico(?![^;\s])|[l|L]ogico(?![^;\s])|[e|E]ntero(?![a-zA-Z0-9])|[R|r]eal(?![^;\s])'

    def t_CONSTANTES(self, t):
        r'[c|C]onstantes(?![\S])'

    def t_VARIABLES(self, t):
        r'[V|v]ariables(?![\S])'

    def t_PROGRAMA(self, t):
        r'[p|P]rograma(?![a-zA-Z0-9])'

    def t_FIN(self, t):
        r'[f|F]in(?![^;^ \S])'

    def t_DE(self, t):
        r'[d|D]e(?![\S])'

    def t_FUNCION(self, t):
        r'[f|F]uncion(?![^;^ \s])'

    def t_PROCEDIMIENTO(self, t):
        r'[p|P]rocedimiento(?![^;^ \s])'

    def t_INICIO(self, t):
        r'[i|I]nicio(?![\S])'

    def t_LIMPIA(self, t):
        r'[l|L]impia(?![\S])'

    def t_SI(self, t):
        r'[s|S]i(?![\S])'

    def t_DESDE(self, t):
        r'[d|D]esde(?![\S])'

    def t_REPETIR(self, t):
        r'[r|R]epetir(?![\S])'

    def t_MIENTRAS(self, t):
        r'[m|M]ientras(?![\S])'

    def t_CUANDO(self, t):
        r'[c|C]uando(?![\S])'

    def t_REGRESA(self, t):
        r'[r|R]egresa(?![^\(\S])'

    def t_IMPRIMENL(self, t):
        r'[i|I]mprimenl(?![a-zA-Z0-9])'

    def t_IMPRIME(self, t):
        r'|[i|I]mprime(?![a-zA-Z0-9])'

    def t_LEE(self, t):
        r'[l|L]ee(?![^\(\s])'

    def t_INTERRUMPE(self, t):
        r'[i|I]nterrumpe(?![\S])'

    def t_CONTINUA(self, t):
        r'[c|C]ontinua(?![\S])'

    def t_HACER(self, t):
        r'[h|H]acer(?![\S])'

    def t_SINO(self, t):
        r'[s|S]ino(?![\S])'

    def t_EL(self, t):
        r'[e|E]l(?![\S])'

    def t_VALOR(self, t):
        r'[v|V]alor(?![\S])'

    def t_HASTA(self, t):
        r'[h|H]asta(?![\S])'

    def t_QUE(self, t):
        r'[q|Q]ue(?![\S])'

    def t_SE(self, t):
        r'[S|s]e(?![\S])'

    def t_CUMPLA(self, t):
        r'[c|C]umpla(?![\S])'

    def t_SEA(self, t):
        r'[s|S]ea(?![\S])'


    def t_OTRO(self, t):
        r'[o|O]tro(?![^:\S])'

    def t_PAL_RES(self, t):
        r'[i|I]ncr(?![\S])|[d|D]ecr(?![\S])'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "PAL_RES"
            self.add_lex("PAL-RES", t.value)

    def t_OP_REL(self, t):
        r'=|<>|<|>|<=|>='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-REL"
            self.add_lex("OP-REL", t.value)


    def t_O(self, t):
        r'o(?![\S])'

    def t_Y(self, t):
        r'y(?![\S])'

    def t_NO(self):
        r'|no(?![\S])'


    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "IDENT"
            self.add_lex("IDENT", t.value)

    def t_CTE_REAL(self, t):
        r'[0-9][\.][0-9]+(?![a-zA-Z_]+)'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-REAL"
            self.add_lex("CTE-REAL", t.value)

    def t_ignore_CTE_REAL_NON_NUM(self, t):
        r'[1-9][\.][a-zA-Z0-9]+'
        self.add_err("Decimal points contains non number values", t.value, t.lexer.lineno)

    def t_ignore_CTE_REAL_ENDING_BAD(self, t):
        r'[1-9][\.](?![ \s^a-zA-Z0-9])'
        self.add_err("Not number after point", t.value, t.lexer.lineno)

    def t_CTE_ENTERA(self, t):
        r'[1-9][0-9]*(?![a-zA-Z$\#\?])'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-ALFA"
            self.add_lex("CTE-ALFA", t.value)

    def t_CTE_ENTERA_NON_NUM(self, t):
        r'[1-9][0-9]*[a-zA-Z$\#\?]+'
        self.add_err("Unknown character for integer value", t.value, t.lexer.lineno)

    def t_OP_ASIG(self, t):
        r':='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-ASIG"
            self.add_lex("OP-ASIG", t.value)

    def t_PAREN_EMPIEZA(self, t):
        r'\('

    def t_PAREN_TERMINA(self, t):
        r'\)'

    def t_CORCHETE_EMPIEZA(self, t):
        r'\['

    def t_CORCHETE_TERMINA(self, t):
        r'\['

    def t_PUNTOS_DOBLES(self, t):
        r':'

    def t_PUNTO_COMA(self, t):
        r';'

    def t_PUNTO(self, t):
        r'.'

    def t_COMA(self, t):
        r','

    def t_OP_ARIT(self, t):
        r'[\+\*/%/\^-]'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-ARIT"
            self.add_lex("OP-ARIT", t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        t.lexer.skip(1)

    def build_lex(self, **kwargs):
        self.lex = lex.lex(module=self, **kwargs)

    def show_lex_cmp(self):
        for value, lex_cmp in self.lexemas.items():
            print('<{0}> : {1}'.format(lex_cmp, value))

    # Append to the .lex file the lex components and their values
    def add_lex(self, lex_cmp, value):
        if self.file_name != "":
            self.output_file.write("<" + lex_cmp + "> : " + value + "\n")

    # Append to the .err file the errors that may be found
    def add_err(self, lex_error, val, line):
        self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")

    # Close the files to prevent further errors when reopening
    def close_file(self):
        self.output_file.close()
        self.err_file.close()



