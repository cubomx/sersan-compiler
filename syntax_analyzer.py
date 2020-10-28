import ply.yacc as yacc
from lex_analyzer import Lexer

class Syntax(object):
    tokens = Lexer.tokens
    def p_programa(self, p):
        'program : constantes variables protfuncproc funproc PROGRAMA block FIN DE PROGRAMA'

    def p_variables(self, p):
        'variables : VARIABLES gpovars'
        print("variables")

    def p_gpovars(self, p):
        'gpovars : gpoids PUNTOS_DOBLES TIPO PUNTO_COMA gpovars'
        print(p)

    def p_gpovarsEmpty(self, p):
        'gpovars : empty'
        print(p)

    def p_gpoids(self, p):
        'gpoids : IDENT dimens opasig COMA gpoids'
        print(p)

    def p_gpoidsEmpty(self, p):
        'gpoids : empty'
        print(p)

    def p_dimens(self, p):
        'dimens : CORCHETE_EMPIEZA valor CORCHETE_TERMINA dimens'
        print(p)

    def p_dimensEmpty(self, p):
        'dimens : empty'
        print(p)

    def p_opasig1(self, p):
        'opasig : OP_ASIG CTE_ENTERA'
        print(p)

    def p_opasig2(self, p):
        'opasig : OP_ASIG IDENT'
        print(p)

    def p_opasigEmpty(self, p):
        'opasig : empty'
        print(p)

    def p_valor(self, p):
        '''valor : CTE_ENTERA
                 | IDENT
        '''
        print(p)

    def p_constantes(self, p):
        'constantes : CONSTANTES IDENT OP_ASIG cantidad PUNTO_COMA grupoconst'
        p[0] += 'CONSTANTES'

    def p_cantidad(self, p):
        '''cantidad : CTE_ENTERA
                    | CTE_REAL'''
        if p.type == "CTE_ENTERA":
            p[0] += 'CTE_ENTERA'
        else:
            p[0] += 'CTE_REAL'

    def p_grupoconst(self, p):
        'grupoconst : constantes'

    def p_grupoconstEmpty(self, p):
        'gpoconst : empty'

    def p_protfuncproc1(self, p):
        'protfuncproc : protfunc'

    def p_protfuncproc2(self, p):
        'protfuncproc : protpoc protfuncproc'

    def p_protfunprocEmpty(self, p):
        'protfuncproc : empty'

    def p_protfunc(self, p):
        'protfunc : funcion IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'

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

    def p_maspars(self, p):
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

    def p_estatuto(self, p):
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
        'bckesp : emtpy'

    def p_desde(self, p):
        'desde : DESDE EL VALOR DE asigna HASTA exp bckesp'

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

    def p_udim(self, p):
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

    def p_empty(self, p):
        'empty :'
        print(p)
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

