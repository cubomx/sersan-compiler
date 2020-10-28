import ply.lex as lex
from ply import yacc


class Lexer(object):
    tokens = (
    'IDENT', 'OP_ARIT', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES', 'OP_REL', 'CTE_ENTERA', 'COMMENT', 'CTE_REAL_NON_NUM',
    'CTE_REAL_ENDING_BAD', 'CTE_ENTERA_NON_NUM', 'VARIABLES', 'CONSTANTES', 'OP_ASIG', 'TIPO','PAREN_EMPIEZA', 'PAREN_TERMINA', 'CORCHETE_EMPIEZA',
    'CORCHETE_TERMINA', 'PUNTOS_DOBLES', 'PUNTO_COMA', 'PUNTO', 'COMA', 'FIN', 'DE', 'PROGRAMA', 'FUNCION', 'PROCEDIMIENTO', 'INICIO', 'LIMPIA',
    'SI', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'REGRESA', 'IMPRIME', 'IMPRIMENL', 'LEE', 'INTERRUMPE', 'CONTINUA', 'HACER', 'SINO', 'EL',
    'VALOR',  'QUE', 'SE', 'CUMPLA', 'SEA', 'OTRO', 'Y', 'O', 'NO', 'MAS', 'MENOS', 'MULTI', 'DIV', 'MOD', 'POTENCIA', 'VERDADERO', 'FALSO', 'HASTA')
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
        pass

    def t_CTE_ALFA(self, t):
        r'"[a-zA-Z0-9_ \[\]\)\(<:\¿\?,\$\#\'\?\!\¡/=*+-\^{}%°\|]*"'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-ALFA"
            self.add_lex("CTE-ALFA", t.value)
        return t

    def t_TIPO(self, t):
        r'[a|A]lfabetico(?![a-zA-Z0-9])|[l|L]ogico(?![a-zA-Z0-9])|[e|E]ntero(?![a-zA-Z0-9])|[R|r]eal(?![a-zA-Z0-9])'
        return t

    def t_CONSTANTES(self, t):
        r'[c|C]onstantes(?![\S])'
        return t

    def t_VARIABLES(self, t):
        r'[V|v]ariables(?![\S])'
        return t

    def t_PROGRAMA(self, t):
        r'[p|P]rograma(?![a-zA-Z0-9])'
        return t

    def t_FIN(self, t):
        r'[f|F]in(?![^;^ \S])'
        return t

    def t_DE(self, t):
        r'[d|D]e(?![\S])'
        return t

    def t_FUNCION(self, t):
        r'[f|F]uncion(?![^;^ \s])'
        return t

    def t_PROCEDIMIENTO(self, t):
        r'[p|P]rocedimiento(?![^;^ \s])'
        return t

    def t_INICIO(self, t):
        r'[i|I]nicio(?![\S])'
        return t

    def t_LIMPIA(self, t):
        r'[l|L]impia(?![\S])'
        return t

    def t_SI(self, t):
        r'[s|S]i(?![\S])'
        return t

    def t_DESDE(self, t):
        r'[d|D]esde(?![\S])'
        return t

    def t_REPETIR(self, t):
        r'[r|R]epetir(?![\S])'
        return t

    def t_MIENTRAS(self, t):
        r'[m|M]ientras(?![\S])'
        return t

    def t_CUANDO(self, t):
        r'[c|C]uando(?![\S])'
        return t

    def t_REGRESA(self, t):
        r'[r|R]egresa(?![^\(\S])'
        return t

    def t_IMPRIMENL(self, t):
        r'[i|I]mprimenl(?![a-zA-Z0-9])'
        return t

    def t_IMPRIME(self, t):
        r'[i|I]mprime(?![a-zA-Z0-9])'
        return t

    def t_LEE(self, t):
        r'[l|L]ee(?![^\(\s])'
        return t

    def t_INTERRUMPE(self, t):
        r'[i|I]nterrumpe(?![\S])'
        return t

    def t_CONTINUA(self, t):
        r'[c|C]ontinua(?![\S])'
        return t

    def t_HACER(self, t):
        r'[h|H]acer(?![\S])'
        return t

    def t_SINO(self, t):
        r'[s|S]ino(?![\S])'
        return t

    def t_EL(self, t):
        r'[e|E]l(?![\S])'
        return t

    def t_VALOR(self, t):
        r'[v|V]alor(?![\S])'
        return t

    def t_HASTA(self, t):
        r'[h|H]asta(?![\S])'
        return t

    def t_QUE(self, t):
        r'[q|Q]ue(?![\S])'
        return t

    def t_SE(self, t):
        r'[S|s]e(?![\S])'
        return t

    def t_CUMPLA(self, t):
        r'[c|C]umpla(?![\S])'
        return t

    def t_SEA(self, t):
        r'[s|S]ea(?![\S])'
        return t


    def t_OTRO(self, t):
        r'[o|O]tro(?![^:\S])'
        return t

    def t_PAL_RES(self, t):
        r'[i|I]ncr(?![\S])|[d|D]ecr(?![\S])'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "PAL_RES"
            self.add_lex("PAL-RES", t.value)
        return t

    def t_OP_REL(self, t):
        r'=|<>|<|>|<=|>='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-REL"
            self.add_lex("OP-REL", t.value)
        return t


    def t_O(self, t):
        r'o(?![\S])'
        return t

    def t_Y(self, t):
        r'y(?![\S])'
        return t

    def t_NO(self, t):
        r'no(?![\S])'
        return t

    def t_VERDADERO(self, t):
        r'[v|V]erdadero(?![\S])'
        return t

    def t_FALSO(self, t):
        r'[f|F]also(?![\S])'
        return t


    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "IDENT"
            self.add_lex("IDENT", t.value)
        return t

    def t_CTE_REAL(self, t):
        r'[0-9][\.][0-9]+(?![a-zA-Z_]+)'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-REAL"
            self.add_lex("CTE-REAL", t.value)
        return t

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
        return t

    def t_CTE_ENTERA_NON_NUM(self, t):
        r'[1-9][0-9]*[a-zA-Z$\#\?]+'
        self.add_err("Unknown character for integer value", t.value, t.lexer.lineno)

    def t_OP_ASIG(self, t):
        r':='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-ASIG"
            self.add_lex("OP-ASIG", t.value)
        return t

    def t_PAREN_EMPIEZA(self, t):
        r'\('
        return t

    def t_PAREN_TERMINA(self, t):
        r'\)'
        return t

    def t_CORCHETE_EMPIEZA(self, t):
        r'\['
        return t

    def t_CORCHETE_TERMINA(self, t):
        r'\['
        return t

    def t_PUNTOS_DOBLES(self, t):
        r':'
        return t

    def t_PUNTO_COMA(self, t):
        r'\;'
        return t

    def t_PUNTO(self, t):
        r'\.'
        return t

    def t_COMA(self, t):
        r','
        return t

    def t_MAS(self, t):
        r'[\+]'
        return t

    def t_MENOS(self, t):
        r'[\-]'
        return t

    def t_MOD(self, t):
        r'[\%]'
        return t

    def t_MULTI(self, t):
        r'[\*]'
        return t

    def t_DIV(self, t):
        r'[\/]'
        return t

    def t_POTENCIA(self, t):
        r'[\^]'
        return t

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



