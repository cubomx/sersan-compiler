import ply.yacc as yacc
from lex_analyzer import Lexer

class Syntax(object):
    tokens = Lexer.tokens
    precedence = (
        ('right', 'IDENT', 'INICIO', 'SI', 'MIENTRAS'),
        ('right', 'PROCEDIMIENTO', 'FUNCION'),
        ('right', 'CONSTANTES', 'VARIABLES'),
        ('right', 'OP_ASIG'),
        ('left', 'OP_REL'),
        ('left', 'MOD'),
        ('left', 'MAS', 'MENOS'),
        ('left', 'MULTI', 'DIV'),
        ('left', 'PAREN_EMPIEZA', 'PAREN_TERMINA'),
    )

    def p_programa(self, p):
        'program : constantes variables protfuncproc funcproc PROGRAMA block FIN DE PROGRAMA'

    def p_variables(self, p):
        'variables : VARIABLES gpovars'

    def p_variablesEmpty(self, p):
        'variables : empty'

    def p_gpovars(self, p):
        '''gpovars : gpoids PUNTOS_DOBLES TIPO PUNTO_COMA gpovars
                   | gpoids PUNTOS_DOBLES TIPO PUNTO_COMA
        '''

    def p_gpovarsEmpty(self, p):
        'gpovars : empty'

    def p_gpoids(self, p):
        '''gpoids : IDENT dimens COMA gpoids
                  | IDENT dimens
                  | IDENT opasig COMA gpoids
                  | IDENT COMA gpoids
                  '''


    def p_gpoidsEmpty(self, p):
        'gpoids : empty'

    def p_dimens(self, p):
        'dimens : CORCHETE_EMPIEZA valor CORCHETE_TERMINA dimens'

    def p_dimensEmpty(self, p):
        'dimens : empty'

    def p_opasig1(self, p):
        'opasig : OP_ASIG CTE_ENTERA'

    def p_opasig2(self, p):
        'opasig : OP_ASIG IDENT'

    def p_opasigEmpty(self, p):
        'opasig : empty'

    def p_valor(self, p):
        '''valor : CTE_ENTERA
                 | IDENT
        '''

    def p_constantes(self, p):
        '''constantes : CONSTANTES grupoconst
        '''


    def p_constantesEmpty(self, p):
        'constantes : empty'


    def p_grupoconst(self, p):
        '''grupoconst : IDENT OP_ASIG CTE_REAL PUNTO_COMA
                      | IDENT OP_ASIG CTE_ENTERA PUNTO_COMA
                      | IDENT OP_ASIG CTE_REAL PUNTO_COMA grupoconst
                      | IDENT OP_ASIG CTE_ENTERA PUNTO_COMA grupoconst
        '''

    def p_grupoconstEmpty(self, p):
        'grupoconst : empty'

    def p_protfuncproc(self, p):
        '''protfuncproc : protfunc protfuncproc
                        | protproc protfuncproc'''

    def p_protfunprocEmpty(self, p):
        'protfuncproc : empty'

    def p_protfunc(self, p):
        'protfunc : FUNCION IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'

    def p_protproc(self, p):
        'protproc : PROCEDIMIENTO IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTO_COMA'

    def p_params(self, p):
        'params : gpopars PUNTOS_DOBLES TIPO otrospars'

    def p_paramsEmpty(self, p):
        'params : empty'

    def p_params2(self, p):
        'otrospars : PUNTO_COMA params'

    def p_params2Empty(self, p):
        'otrospars : empty'

    def p_gpopars(self, p):
        'gpopars : IDENT maspars'

    def p_maspars(self, p):
        'maspars : COMA gpopars'

    def p_masparsEmpty(self, p):
        'maspars : empty'

    def p_funcproc(self, p):
        '''funcproc : procedimiento funcproc
                    | funcion funcproc
        '''

    def p_funcprocEmpty(self, p):
        'funcproc : empty'

    def p_procedimiento(self, p):
        'procedimiento : PROCEDIMIENTO IDENT PAREN_EMPIEZA params PAREN_TERMINA variables INICIO block FIN DE PROCEDIMIENTO PUNTO_COMA'

    def p_funcion(self, p):
        'funcion : FUNCION IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO variables INICIO block FIN DE FUNCION PUNTO_COMA'

    def p_block(self, p):
        'block : estatuto PUNTO_COMA block'

    def p_blockEmpty(self, p):
        'block : empty'

    def p_estatuto(self, p):
        '''estatuto : si
                    | LIMPIA
                    | desde
                    | repetir
                    | mientras
                    | cuando
                    | regresa
                    | asigna
                    | lproc
                    | imprime
                    | imprimenl
                    | lee
                    | INTERRUMPE
                    | CONTINUA
        '''

    def p_estatutoEmpty(self, p):
        'estatuto : empty'

    def p_si(self, p):
        'si : SI PAREN_EMPIEZA exprlog PAREN_TERMINA HACER bckesp sino'

    def p_sino(self, p):
        'sino : SINO bckesp'

    def p_sinoEmpty(self, p):
        'sino : empty'

    def p_bckesp(self, p):
        'bckesp : estatuto INICIO block FIN'

    def p_bckespEmpty(self, p):
        'bckesp : empty'

    def p_desde(self, p):
        'desde : DESDE EL VALOR DE asigna HASTA expr bckesp'

    def p_repetir(self, p):
        'repetir : REPETIR block HASTA QUE PAREN_EMPIEZA exprlog PAREN_TERMINA'

    def p_mientras(self, p):
        'mientras : MIENTRAS SE CUMPLA QUE exprlog bckesp'

    def p_asigna(self, p):
        'asigna : IDENT udim OP_ASIG exprlog'

    def p_cuando(self, p):
        'cuando : CUANDO EL VALOR DE IDENT INICIO gposea otro FIN'

    def p_otro(self, p):
        'otro : OTRO PUNTOS_DOBLES bckesp'

    def p_otroEmpty(self, p):
        'otro : empty'

    def p_gposea(self, p):
        'gposea : SEA gpoconst PUNTOS_DOBLES bckesp gposea'

    def p_gposeaEmpty(self, p):
        'gposea : empty'

    def p_gpoconst(self, p):
        'gpoconst : CTE_ALFA masgpoconst'

    def p_masgpoconst(self, p):
        'masgpoconst : COMA gpoconst'

    def p_masgpoconstEmpty(self, p):
        'masgpoconst : empty'

    def p_regresa(self, p):
        'regresa : REGRESA PAREN_EMPIEZA exprlog PAREN_TERMINA'

    def p_udim(self, p):
        'udim : expr udim '

    def p_udimEmpty(self, p):
        'udim : empty'

    def p_exprlog(self, p):
        'exprlog : opy o'

    def p_o(self, p):
        'o : O exprlog'

    def p_oEmpty(self, p):
        'o : empty'

    def p_opy(self, p):
        '''opy : opno
               | opno Y opy
        '''

    def p_opno(self, p):
        '''opno : oprel
                | NO oprel
        '''

    def p_oprel(self, p):
        '''oprel : expr
                 | expr OP_REL oprel
         '''


    def p_expr(self, p):
        '''expr : multi
                | MAS expr
                | MENOS expr
        '''


    def p_multi(self, p):
        '''multi : expo
                 | expo MULTI
                 | expo DIV
                 | expo MOD multi
        '''

    def p_expo(self, p):
        '''expo : signo
                | signo POTENCIA expo
        '''

    def p_signo(self, p):
        '''signo : termino
                 | MENOS termino
        '''

    def p_termino(self, p):
        '''termino : IDENT lfunc
                   | IDENT udim
                   | PAREN_EMPIEZA exprlog PAREN_TERMINA
                   | CTE_ENTERA
                   | CTE_REAL
                   | CTE_ALFA
                   | VERDADERO
                   | FALSO
        '''

    def p_lproc(self, p):
        'lproc : IDENT PAREN_EMPIEZA uparams PAREN_TERMINA'

    def p_lfunc(self, p):
        'lfunc : IDENT PAREN_EMPIEZA uparams PAREN_TERMINA'

    def p_imprime(self, p):
        'imprime : IMPRIME PAREN_EMPIEZA gpoexp PAREN_TERMINA'

    def p_imprimenl(self, p):
        'imprimenl : IMPRIMENL PAREN_EMPIEZA gpoexp PAREN_TERMINA'

    def p_lee(self, p):
        '''lee : LEE PAREN_EMPIEZA IDENT PAREN_TERMINA
               | LEE PAREN_EMPIEZA IDENT dimens PAREN_TERMINA
        '''




    def p_gpoexp(self, p):
        '''gpoexp : exprlog
                  | exprlog COMA gpoexp
        '''

    def p_uparams(self, p):
        '''uparams : exprlog
                   | exprlog COMA uparams
        '''

    def p_uparamsEmpty(self, p):
        'uparams : empty'


    def p_empty(self, p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            print("Syntax error at token", p.type)
            print("Syntax error at '%s'" % p.value)
            print("line : '%s'" % p.lineno)
            print("column: '%s'" % p.lexpos)
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

