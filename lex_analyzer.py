import ply.lex as lex


class Lexer(object):
    tokens = ('IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES', 'OP_REL', 'CTE_ENTERA', 'COMMENT')

    # when finding new line /n
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # the following functions are code to do when finding some token

    def t_COMMENT(self, t):
        r'//'
        print("COMENTARIO " + t.value)

    def t_CTE_ALFA(self, t):
        r'"[a-zA-Z0-9_ \[\]\)\(<:\¿\?,\$\#\'\?\!\¡/=*+-\^{}%°\|]*"'
        print("CADENA " + t.value)

    def t_PAL_RES(self, t):
        r'[c|C]onstantes(?![\S])|[V|v]ariables(?![\S])|[R|r]eal(?![^;\s])|[a|A]lfabetico(?![^;\s])|[l|L]ogico(?![^;\s])|[e|E]ntero(?![a-zA-Z0-9])'\
        '|[f|F]uncion(?![^;^ \s])|[i|I]nicio(?![\S])|[f|F]in(?![^;^ \S])|[d|D]e(?![\S])|[p|P]rocedimiento(?![^;^ \s])|[r|R]egresa(?![^\(\S])|[s|S]i(?![\S])'\
        '|[h|H]acer(?![\S])|[s|S]ino(?![\S])|[c|C]uando(?![\S])|[e|E]l(?![\S])|[v|V]alor(?![\S])|[s|S]ea(?![\S])|[o|O]tro(?![^:\S])|[d|D]esde(?![\S])'\
        '|[h|H]asta(?![\S])|[i|I]ncr(?![\S])|[d|D]ecr(?![\S])|[r|R]epetir(?![\S])|[q|Q]ue(?![\S])|[m|M]ientras(?![\S])|[S|s]e(?![\S])|[c|C]umpla(?![\S])'\
        '|[c|C]ontinua(?![\S])|[i|I]nterrumpe(?![\S])|[l|L]impia(?![\S])|[l|L]ee(?![^\(\s])|'\
        '[i|I]mprimenl(?![a-zA-Z0-9])|[i|I]mprime(?![a-zA-Z0-9])|[p|P]rograma(?![a-zA-Z0-9])'
        print("RESERVADA " + t.value)


    def t_OP_REL(self, t):
        r'=|<>|<|>|<=|>='
        print("RELACIONAL " + t.value)

    def t_OP_LOG(self, t):
        r'y(?![\S])|o(?![\S])|no(?![\S])'
        print("LOGICO " + t.value)

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        print("IDENT " + t.value)

    def t_CTE_REAL(self, t):
        r'[1-9][\.][0-9]*'
        print("CTE-REAL " + t.value)

    def t_CTE_ENTERA(self, t):
        r'[1-9][0-9]*'
        print("CTE-ENTERA " + t.value)

    def t_OP_ASIG(self, t):
        r':='
        print("ASIGNACION " + t.value)

    def t_DELIM(self, t):
        r'[)(;\]\[:\.,]'
        print("DELIM " + t.value)


    def t_OP_ARIT(self, t):
        r'[\+\*/%/\^-]'
        print("OP-ARIT " + t.value)


    def t_error(self, t):
        # print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build_lex(self, **kwargs):
        self.lex = lex.lex(module=self, **kwargs)


