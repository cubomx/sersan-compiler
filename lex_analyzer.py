import ply.lex as lex


class Lexer(object):
    tokens = ('IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES')
    reserved = ('constantes', 'variables', 'real', 'alfabetico', 'logico', 'entero', 'funcion',
                'inicio', 'fin', 'de', 'procedimiento', 'regresa', 'si', 'hacer', 'sino',
                'cuando', 'el', 'valor', 'sea', 'otro', 'desde', 'hasta', 'incr', 'decr',
                'repetir', 'que', 'mientras', 'se', 'cumpla', 'continua', 'interrumpe', 'limpia',
                'lee', 'imprime', 'imprimenl')
    # when finding new line /n

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # the following functions are code to do when finding some token

    def t_CTE_ALFA(self, t):
        r'[\"][.]+[\"]'
        print("CADENA " + t.value)

    def t_PAL_RES(self, t):
        r'constantes|variables|real|alfabetico|logico|entero|funcion|inicio|fin|de|procedimiento|regresa|si|hacer|sino|cuando'\
        '|el|valor|sea|otro|desde|hasta|incr|decr|repetir|que|mientras|se|cumpla|continua|interrumpe|limpia|lee|imprime|imprimenl'
        print("RESERVADA " + t.value)

    def t_OP_LOG(self, t):
        r'[y|o|no]'
        print("LOGICO " + t.value)

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        print("IDENT " + t.value)

    def t_CTE_REAL(self, t):
        r'[1-9][0-9]*'
        print("CTE-REAL " + t.value)


    def t_DELIM(self, t):
        r'[)(;\]\[]'
        print("DELIM " + t.value)


    def t_OP_ARIT(self, t):
        r'[+*/%^-]'
        print("OP-ARIT " + t.value)





    def t_error(self, t):
        # print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build_lex(self, **kwargs):
        self.lex = lex.lex(module=self, **kwargs)


