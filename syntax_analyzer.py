import ply.yacc as yacc
from lex_analyzer import Lexer
from collections import deque
from semantic import SymbolTable

class Syntax(object):
    tokens = Lexer.tokens
    pila = deque()
    estatutos = Lexer.estatutos
    line_analyzing = list()
    precedence = (
        ('left', 'IDENT', 'INICIO', 'SI', 'MIENTRAS'),
        ('right', 'PROCEDIMIENTO', 'FUNCION'),
        ('right', 'CONSTANTES', 'VARIABLES'),
        ('right', 'OP_ASIG'),
        ('left', 'OP_REL'),
        ('left', 'MOD'),
        ('left', 'MAS', 'MENOS'),
        ('left', 'MULTI', 'DIV'),
        ('right', 'PROTOTIPOS'),
        ('right', 'CORCHETE_EMPIEZA', 'CORCHETE_TERMINA'),
        ('left', 'PAREN_TERMINA'),
        ('left', 'PAREN_EMPIEZA'),
        ('right', 'PUNTO_COMA'),
        ('left', 'FIN')

    )

    def __init__(self, filename):
        self.file_name = filename
        open(self.file_name + ".err", 'w').close()
        self.err_file = open(self.file_name + ".err", "a")
        self.symTable_ = SymbolTable(self.err_file, filename)

    def p_programa(self, p):
        'program : constantes variables protfuncproc funcproc PROGRAMA block FIN DE PROGRAMA PUNTO'

    def p_variables(self, p):
        'variables : VARIABLES gpovars'

    def p_variablesEmpty(self, p):
        'variables : empty'

    def p_gpovars(self, p):
        '''gpovars : gpoids PUNTOS_DOBLES TIPO PUNTO_COMA gpovars
                   | gpoids PUNTOS_DOBLES TIPO PUNTO_COMA
        '''
        self.pila.append(p[3])
        self.symTable_.var_add(self.pila)


    def p_gpovarsEmpty(self, p):
        'gpovars : empty'

    def p_gpovars_error1(self, p):
        '''gpovars : gpoids error TIPO PUNTO_COMA gpovars
                   | gpoids error TIPO PUNTO_COMA
        '''
        self.add_err("Missing ':' after variable declaration", '', p.lineno(2))

    def p_gpovars_error2(self, p):
        '''gpovars : gpoids PUNTOS_DOBLES error PUNTO_COMA gpovars
                   | gpoids PUNTOS_DOBLES error PUNTO_COMA
        '''
        print("Missing <type> in variable definition")
        self.add_err("Missing <type> in variable definition", '', p.lineno(4))


    def p_gopids_(self, p):
        '''gpoids : IDENT COMA gpoids2
                    | IDENT opasig COMA gpoids2
                    | IDENT gpoids2
                    | IDENT
                    '''
        self.pila.append(p[1])
        self.pila.append("###")

    def p_gpoids_2(self, p):
        '''gpoids : IDENT dimens COMA gpoids2
                  | IDENT dimens
                  '''
        print(p[1])
        self.pila.append(p[1])
        self.pila.append("DIM")
        self.pila.append("###")



    def p_gpoids2_2(self, p):
        '''gpoids2 : IDENT COMA gpoids2
                   | IDENT opasig COMA gpoids2
                   | IDENT
        '''
        self.pila.append(p[1])

    def p_gpoids2(self, p):
        '''gpoids2 : IDENT dimens COMA gpoids2
                  | IDENT dimens

                  '''
        print(p[1])
        print(p[2])
        self.pila.append(p[1])
        self.pila.append("DIM")



    def p_gpoidsError(self, p):
        '''gpoids : IDENT dimens error gpoids
                  | IDENT error gpoids
                  | IDENT opasig error gpoids
        '''

        print("Missing ',' between individual variable declaration")
        self.add_err("Missing ',' between individual variable declaration", '', p.lineno(2))


    def p_gpoidsEmpty(self, p):
        'gpoids : empty'

    def p_gpoids2Empty(self, p):
        'gpoids2 : empty'

    def p_dimens(self, p):
        '''dimens : CORCHETE_EMPIEZA valor CORCHETE_TERMINA dimens'''
        print("dimension")
        self.pila.append("[]")


    def p_dimensEmpty(self, p):
        'dimens :'

    def p_dimens_error1(self, p):
        '''dimens : CORCHETE_EMPIEZA valor error dimens'''
        self.add_err("Missing ']' to close dimensions", '', p.lineno(1))

    def p_dimens_erro2(self, p):
        '''dimens : error valor CORCHETE_TERMINA dimens'''
        self.add_err("Missing '[' of dimension", '', p.lineno(3))


    def p_opasig1(self, p):
        'opasig : OP_ASIG CTE_ENTERA'

    def p_opasig2(self, p):
        'opasig : OP_ASIG IDENT'

    def p_opasigEmpty(self, p):
        'opasig : empty'

    def p_valor(self, p):
        '''valor : exprlog
        '''

    def p_constantes(self, p):
        '''constantes : CONSTANTES grupoconst
        '''


    def p_constantesEmpty(self, p):
        'constantes : empty'


    def p_grupoconstReal(self, p):
        '''grupoconst : IDENT OP_ASIG CTE_ENTERA PUNTO_COMA
                      | IDENT OP_ASIG CTE_ENTERA PUNTO_COMA grupoconst
        '''
        self.pila.append(p[1])
        self.pila.append("E")
        self.pila.append(p[3])

    def p_grupoconstEntera(self, p):
        '''grupoconst : IDENT OP_ASIG CTE_REAL PUNTO_COMA
                      | IDENT OP_ASIG CTE_REAL PUNTO_COMA grupoconst
        '''
        self.pila.append(p[1])
        self.pila.append("R")
        self.pila.append(p[3])
        self.pila.append("%%%")
        self.symTable_.const_add(self.pila)

    def p_grupoconstEmpty(self, p):
        'grupoconst : empty'

    def p_startproto(self, p):
        'protfuncproc : PROTOTIPOS gpofuncproc FIN DE PROTOTIPOS PUNTO_COMA'
        print("PROTOTIPOS")

    def p_startprotoEmpty(self, p):
        'protfuncproc : empty'

    def p_protfuncproc(self, p):
        '''gpofuncproc : protfunc
                        | protproc
                        | protproc gpofuncproc
                        | protfunc gpofuncproc
                        '''

    def p_protfunc(self, p):
        'protfunc : FUNCION IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'

    def p_protfunc_error1(self, p):
        'protfunc : FUNCION error PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'
        self.add_err("Missing identifier on function prototype", '', p.lineno(1))

    def p_protproc(self, p):
        'protproc : PROCEDIMIENTO IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTO_COMA'

    def p_protproc_error1(self, p):
        'protproc : PROCEDIMIENTO error PAREN_EMPIEZA params PAREN_TERMINA  PUNTO_COMA'
        self.add_err("Missing identifer on procedure prototype", '', p.lineno(1))

    def p_protprocEmpty(self, p):
        'protproc : empty'

    def p_params(self, p):
        'params : gpopars PUNTOS_DOBLES TIPO otrospars'

    def p_paramsEmpty(self, p):
        'params : empty'

    def p_params_error1(self, p):
        'params : gpopars PUNTOS_DOBLES error otrospars'
        self.add_err("Missing <type> of param", '', p.lineno(2))

    def p_params_error2(self, p):
        'params : gpopars error TIPO otrospars'
        self.add_err("Missing ':' before type of param", '', p.lineno(1))

    def p_params2(self, p):
        'otrospars : PUNTO_COMA params'

    def p_params2Empty(self, p):
        'otrospars : empty'

    def p_gpopars(self, p):
        '''gpopars : IDENT COMA gpopars
                   | IDENT
        '''

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
        '''block : estatuto puntoc block
                 | estatuto puntoc
        '''
        print("block linea: ")

    def p_puntoc(self, p):
        'puntoc : PUNTO_COMA'

    def p_semicolon(self, p):
        '''block : estatuto error
                 | estatuto error block
        '''
        print("Expecting semi-colon at the end of line")
        self.add_err("Expecting semi-colon at the end of line", '', -1)


    def p_estatuto(self, p):
        '''estatuto : si
                    | lfunc
                    | LIMPIA
                    | desde
                    | repetir
                    | mientras
                    | cuando
                    | regresa
                    | asigna
                    | imprime
                    | imprimenl
                    | lee
                    | INTERRUMPE
                    | CONTINUA
        '''
        if p[1] == "imprime": print("yooooooooooooo0000")

    def p_estatutoEmpty(self, p):
        'estatuto : empty'

    def p_si(self, p):
        'si : SI PAREN_EMPIEZA exprlog PAREN_TERMINA HACER bckesp sino'


    def p_sino(self, p):
        'sino : SINO bckesp'

    def p_sinoEmpty(self, p):
        'sino : empty'

    def p_bckesp(self, p):
        '''bckesp : estatuto
                  | INICIO block FIN
                  |'''



    def p_desde(self, p):
        '''desde : DESDE EL VALOR DE asigna HASTA expr DECR CTE_ENTERA bckesp
                 | DESDE EL VALOR DE asigna HASTA expr INCR CTE_ENTERA bckesp
        '''
        print("buen desde")

    def p_desde_error(self, p):
        '''desde : DESDE EL VALOR DE asigna HASTA expr error bckesp'''
        print("Not increment/decrement value in line ", p.lineno(1))
        self.add_err("Not increment/decrement value in line ", '', p.lineno(1))

    '''def p_desde_error2(self, p):
        desde : DESDE error bckesp
        '
        print("Bad scripture of 'DESDE' block")'''



    def p_repetir(self, p):
        'repetir : REPETIR block HASTA QUE PAREN_EMPIEZA exprlog PAREN_TERMINA'
        print("repetir")

    def p_mientras(self, p):
        'mientras : MIENTRAS SE CUMPLA QUE exprlog bckesp'

    def p_asigna(self, p):
        'asigna : IDENT udim OP_ASIG exprlog'

    def p_cuando(self, p):
        'cuando : CUANDO EL VALOR DE IDENT INICIO gposea otro FIN'
        print("cuando")

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
        '''udim : CORCHETE_EMPIEZA expr CORCHETE_TERMINA udim
                | empty
        '''

    def p_exprlog(self, p):
        '''exprlog : opy
                   | opy O exprlog
        '''
        print("he")

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
                | multi MAS expr
                | multi MENOS expr
        '''


    def p_multi(self, p):
        '''multi : expo
                 | expo MULTI multi
                 | expo DIV multi
                 | expo MOD multi
                 | empty
        '''

    def p_expo(self, p):
        '''expo : signo
                | signo POTENCIA expo
        '''

    def p_signo(self, p):
        '''signo : termino
                 | MENOS termino
        '''
        print("signo")

    def p_termino(self, p):
        '''termino : IDENT
                   | CTE_ENTERA
                   | CTE_REAL
                   | CTE_ALFA
                   | VERDADERO
                   | FALSO
        '''
        self.pila.append(p[1])

    def p_terminoNoValor(self, p):
        '''termino :
                   | IDENT udim
                   | lfunc'''
        print("termino")

    def p_lfunc(self, p):
        'lfunc : IDENT parenemp uparams PAREN_TERMINA'
        print("lfunc")

    def p_lfunc_error(self, p):
        'lfunc : IDENT parenemp error PAREN_TERMINA'
        print("Syntax error. Expecting logical expression in function call")
        self.add_err('Expecting logical expression in function call', str(3), p.lineno(3))

    def p_parenEmpieza(self, p):
        'parenemp : PAREN_EMPIEZA'

    def p_imprime(self, p):
        'imprime : IMPRIME PAREN_EMPIEZA gpoexp PAREN_TERMINA'
        self.pila.append("IMPRIME")
        #self.symTable_.imprime(self.pila)

    def p_imprimenl(self, p):
        'imprimenl : IMPRIMENL PAREN_EMPIEZA gpoexp PAREN_TERMINA '
        self.pila.append("IMPRIMENL")

    def p_imprimenl_error(self, p):
        'imprimenl : IMPRIMENL PAREN_EMPIEZA gpoexp error'
        print("Missing parenthesis at end of IMPRIMENL statement ", p.lineno(3))
        self.add_err("Missing parenthesis at end of IMPRIMENL statement ", '', p.lineno(2))

    def p_lee(self, p):
        '''lee : LEE PAREN_EMPIEZA IDENT PAREN_TERMINA
               | LEE PAREN_EMPIEZA IDENT dimens PAREN_TERMINA
        '''
        self.pila.append(p[3])
        self.pila.append("LEE")
        self.symTable_.lee(self.pila)

    def p_gpoexp(self, p):
        '''gpoexp : exprlog
                  | exprlog COMA gpoexp2
        '''

    def p_gpoexp2(self, p):
        '''gpoexp2 : exprlog
                  | exprlog COMA gpoexp2
                  |'''




    def p_uparams(self, p):
        '''uparams : exprlog
                   | exprlog COMA uparams
        '''
        print("yessss")


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
            self.add_err("Syntax error", p.value, p.lineno)
        else:
            print("Syntax error at EOF")


    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    # Append to the .err file the errors that may be found
    def add_err(self, lex_error, val, line):
        if line == -1:
            self.err_file.write("err: " + lex_error + "\n")
        else:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")


