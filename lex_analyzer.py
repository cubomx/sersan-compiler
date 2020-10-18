import ply.lex as lex


class Lexer(object):
    tokens = (
    'IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES', 'OP_REL', 'CTE_ENTERA', 'COMMENT')
    lexemas = dict()

    def __init__(self, filename):
        self.file_name = filename
        self.output_file = open(self.file_name, "a")

    # when finding new line /n
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # the following functions are code to do when finding some token

    def t_COMMENT(self, t):
        r'//[.]'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "COMENTARIO"
            self.add_lex("COMENTARIO", t.value)

    def t_CTE_ALFA(self, t):
        r'"[a-zA-Z0-9_ \[\]\)\(<:\¿\?,\$\#\'\?\!\¡/=*+-\^{}%°\|]*"'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-ALFA"
            self.add_lex("CTE-ALFA", t.value)

    def t_PAL_RES(self, t):
        r'[c|C]onstantes(?![\S])|[V|v]ariables(?![\S])|[R|r]eal(?![^;\s])|[a|A]lfabetico(?![^;\s])|[l|L]ogico(?![^;\s])|[e|E]ntero(?![a-zA-Z0-9])' \
        '|[f|F]uncion(?![^;^ \s])|[i|I]nicio(?![\S])|[f|F]in(?![^;^ \S])|[d|D]e(?![\S])|[p|P]rocedimiento(?![^;^ \s])|[r|R]egresa(?![^\(\S])|[s|S]i(?![\S])' \
        '|[h|H]acer(?![\S])|[s|S]ino(?![\S])|[c|C]uando(?![\S])|[e|E]l(?![\S])|[v|V]alor(?![\S])|[s|S]ea(?![\S])|[o|O]tro(?![^:\S])|[d|D]esde(?![\S])' \
        '|[h|H]asta(?![\S])|[i|I]ncr(?![\S])|[d|D]ecr(?![\S])|[r|R]epetir(?![\S])|[q|Q]ue(?![\S])|[m|M]ientras(?![\S])|[S|s]e(?![\S])|[c|C]umpla(?![\S])' \
        '|[c|C]ontinua(?![\S])|[i|I]nterrumpe(?![\S])|[l|L]impia(?![\S])|[l|L]ee(?![^\(\s])|' \
        '[i|I]mprimenl(?![a-zA-Z0-9])|[i|I]mprime(?![a-zA-Z0-9])|[p|P]rograma(?![a-zA-Z0-9])'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "PAL_RES"
            self.add_lex("PAL-RES", t.value)

    def t_OP_REL(self, t):
        r'=|<>|<|>|<=|>='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-REL"
            self.add_lex("OP-REL", t.value)

    def t_OP_LOG(self, t):
        r'y(?![\S])|o(?![\S])|no(?![\S])'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "LOGICO"
            self.add_lex("LOGICO", t.value)

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "IDENT"
            self.add_lex("IDENT", t.value)

    def t_CTE_REAL(self, t):
        r'[1-9][\.][0-9]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-REAL"
            self.add_lex("CTE-REAL", t.value)

    def t_CTE_ENTERA(self, t):
        r'[1-9][0-9]*'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "CTE-ALFA"
            self.add_lex("CTE-ALFA", t.value)

    def t_OP_ASIG(self, t):
        r':='
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-ASIG"
            self.add_lex("OP-ASIG", t.value)

    def t_DELIM(self, t):
        r'[)(;\]\[:\.,]'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "DELIM"
            self.add_lex("DELIM", t.value)

    def t_OP_ARIT(self, t):
        r'[\+\*/%/\^-]'
        if not t.value in self.lexemas:
            self.lexemas[t.value] = "OP-ARIT"
            self.add_lex("OP-ARIT", t.value)

    def t_error(self, t):
        if t.value[0] == " ":
            print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build_lex(self, **kwargs):
        self.lex = lex.lex(module=self, **kwargs)


    def show_lex_cmp(self):
        for value, lex_cmp in self.lexemas.items():
            print('<{0}> : {1}'.format(lex_cmp, value))

    def add_lex(self, lex_cmp, value):
        if self.file_name != "":
            self.output_file.write("<" + lex_cmp + "> : " + value + "\n")

    def close_file(self):
        self.output_file.close()
