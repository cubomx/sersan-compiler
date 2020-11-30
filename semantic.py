from symbol import Nodo, Instruction, PendingTag
from collections import deque


class SymbolTable:
    def __init__(self, file, filename):
        self.instrucciones = ''
        self.estatutos = ('LIMPIA',
                     'SI', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'REGRESA', 'IMPRIME', 'IMPRIMENL', 'LEE',
                     'INTERRUMPE', 'CONTINUA', 'HACER', 'SINO', 'EL',
                     'VALOR', 'QUE', 'SE', 'CUMPLA', 'SEA', 'OTRO', 'IMPRNL')
        self.nexos = ('Y', 'O', 'NO')
        self.oprel = ('<>', '<=', '>=', '<', '>', '=')
        self.dict = dict()
        self.labels = []
        self.resolvedLabels = []
        self.err_file = file
        self.file_name = filename
        open(self.file_name + ".eje", 'w').close()
        self.eje = open(self.file_name + ".eje", "a")
        self.cont = 1
        self.inner_sentences = deque()
        self.compareTO = ''
        self.labelCont = 1
        self.endCycle = None
        self.endCycleCont = 1
        self.code = deque()
        self.startOfFunction = 1

    def info_to_eje(self):
        self.eje.write(self.get_table())
        self.eje.write(self.print_tags())
        self.eje.write('@\n')
        self.eje.write(self.instrucciones)

    def print_tags(self):
        string_build = ''
        for i in self.resolvedLabels:
            string_build += i.tag + ',I,I,' + str(i.line) + ',0,#'+'\n'
        return string_build


    def programa(self, pila):
        pila.pop()
        print('_P' + ',I' + ',I' + ',' + str(self.startOfFunction))
        lista = deque()
        while len(pila) > 0:
            nxt = pila.pop()
            lista += self.statuto(pila, nxt)

        lista.append(self.add_code_for_latter('OPR', 0, 0, False, None))

        if len(lista) > 0:
            self.take_everything_to_eje(lista)


        self.startOfFunction = self.cont + 1


    def check_Dependencies(self, subdict):
        string_build = ''
        for key, value in subdict.items():
            string_build += value.type + ',' + value.datatype + ',' + str(value.dimens[0]) + ',' + str(value.dimens[1]) + ',' + key + ','
        return string_build



    def __str__(self):
        string = ""
        for key, value in self.dict.items():
            string += key + "," + value.type + "," + value.datatype + "," + str(value.dimens[0]) + "," + str(value.dimens[1]) + ','
            if value.dependency is not None:
                string += self.check_Dependencies(value.dependency)
            string += '#,' + '\n'

        return string

    def get_table(self):
        string = ""
        for key, value in self.dict.items():
            string += key + "," + value.type + "," + value.datatype + "," + str(value.dimens[0]) + "," + str(
                value.dimens[1]) + ','
            if value.dependency is not None:
                string += self.check_Dependencies(value.dependency)
            string += '#,' + '\n'

        return string

    def insert(self, nodo, key):
        self.dict[key] = nodo

    def search(self, key):
        if key in self.dict:
            return self.dict[key]
        return None

    def exists(self, key):
        if key in self.dict:
            return True
        return False

    def const_add(self, pila):
        top = pila.pop()

        while top != '':
            new_nodo = Nodo()
            new_nodo.value = pila.pop()
            new_nodo.type = "C"
            new_nodo.datatype = pila.pop()
            new_nodo.name = pila.pop()

            if self.exists(new_nodo.name):
                self.add_err("Cannot redeclared const ", new_nodo.name, -1)
            else:
                self.dict[new_nodo.name] = new_nodo
            if len(pila) == 0:
                top = ''

    def add_to_table(self, new_nodo):
        if self.exists(new_nodo.name):
            self.add_err("Cannot redeclared variable ", new_nodo.name, -1)
        else:
            self.dict[new_nodo.name] = new_nodo

    def get_type(self, value):
        if value.upper() == 'ENTERO':
            return 'E'
        elif value.upper() == 'ALFABETICO':
            return 'A'
        elif value.upper() == 'REAL':
            return 'R'
        elif value.upper() == 'LOGICO':
            return 'L'



    def checkForParams(self, pila, type_, functProcNode):
        if type_ == 'ENTERO' or type_ == 'ALFABETICO' or type_ == 'REAL' or type_ == 'LOGICO':
            while True:
                name = pila.pop()
                if name == '???':
                    break
                if self.exists(name):
                    newNodo = Nodo()
                    newNodo.type = 'P' # Of parameter
                    newNodo.datatype = self.get_type(type_)
                    newNodo.scope = functProcNode.name
                    search = self.search(name)
                    search.dependency[functProcNode.name] = newNodo
        else:
            pila.append(type_)



    def funcion_prototype(self, pila):
        pila.pop()
        functionNode = Nodo()
        functionNode.name = pila.pop()
        functionNode.type = 'F'
        functionNode.datatype = self.get_type(pila.pop())
        self.add_to_table(functionNode)

        # Now the params
        type_ = pila.pop()
        upp_type = type_.upper()
        self.checkForParams(pila, upp_type, functionNode)

    def procedure_prototype(self, pila):
        pila.pop()
        procNode = self.add_procedure_to_table(pila.pop())

        type_ = pila.pop()
        upp_type = type_.upper()
        self.checkForParams(pila, upp_type, procNode)

    def add_procedure_to_table(self, ident):
        procNode = Nodo()
        procNode.name = ident
        procNode.type = 'P'
        procNode.datatype = 'I'
        self.add_to_table(procNode)
        return procNode


    def procedure(self, pila):

        pila.pop()
        ident = pila.pop()
        if self.exists(ident):
            node = self.search(ident)
            if node.type != 'P':
                self.add_err('Declaration of procedure using a identifier of somehthing else', ident, -1)
            else:
                node.dimens[0] = self.startOfFunction
                self.add_code('OPR', 0, 1)
                self.startOfFunction = self.cont
        else:
            procNode = self.add_procedure_to_table(ident)
            if len(pila)> 0:
                type_ = pila.pop()
                upp_type = type_.upper()
                self.checkForParams(pila, upp_type, procNode)
            procNode.dimens[0] = self.startOfFunction
            self.add_code('OPR', 0, 1)
            self.startOfFunction = self.cont




    def is_valid_value(self, nxt, newNodo, dimension):
        if nxt.isdigit():
            print("hei33333333333333333333333")
            newNodo.dimens[dimension] = int(nxt)
        else:
            try:
                floating = float(nxt)
                self.add_err("Cannot use real number as index", nxt, -1)
            except ValueError:
                search = self.search(nxt)
                if search is not None:
                    if search.datatype == "E":
                        if search.value is not None:
                            newNodo.dimens[dimension] = search.value
                        else:
                            self.add_err("Declaring size of array of not initialized value", search.name, -1)
                    else:
                        self.add_err("Declaring size of array with non integer index", search.name, -1)
                else:
                    self.add_err("Declaring size of array of undefined value", nxt, -1)


    def var_add(self, pila):
        print(pila)
        datatype = self.get_type(pila.pop())
        type_ = 'V'
        new_ = pila.pop()
        if new_ == '###':
            new_ = pila.pop()

        pila_matrices = deque()
        cont = 0
        while True:
            if cont > 0:
                new_ = pila.pop()
            newNodo = Nodo()
            cont += 1
            if new_ == '###':
                break
            elif new_ == 'DIM':
                newNodo.name = pila.pop()
                newNodo.type = type_
                newNodo.datatype = self.get_type(datatype)
                pila_matrices.append(newNodo)
            elif new_ == '[]':
                newNodo = pila_matrices.pop()
                nxt = pila.pop()
                if nxt == "[]":
                    nxt = pila.pop()
                    self.is_valid_value(nxt, newNodo, 1)
                    nxt = pila.pop()

                self.is_valid_value(nxt, newNodo, 0)

                self.add_to_table(newNodo)

            else:
                print(new_)
                newNodo.name = new_
                newNodo.type = type_
                newNodo.datatype = datatype
                newNodo.value = "I"
                self.add_to_table(newNodo)

            if len(pila) == 0:
                break



    # OPCODE --> 20, the operation CODE to show input to the user
    def imprime(self, pila):
        message = ''
        pila.pop()
        message += pila.pop()
        # Take the string to show on console to the queue
        self.add_code('LIT', message, 0)
        # Tell the machine to show the message
        self.add_code('OPR', 0, 20)
        return

    def take_everything_to_eje(self, lista):

        while len(lista) > 0:
            el = lista.pop()
            if el.istTag:
                if not el.pendingTag:
                    tag_ = el.type.split(' ')[1]
                    self.labels.append(PendingTag(el.param_2, tag_))
                else:
                    self.check_tags(el.type, self.cont)
                self.instrucciones += str(self.cont) + ' ' + el.op + ' ' + str(el.param_1) + ',' + str(el.param_2) + "\n"
            else:
                self.instrucciones += str(self.cont) + ' ' + el.op + ' ' + str(el.param_1) + ',' + str(el.param_2) + "\n"
            self.cont += 1



    def check_tags(self, type_, line):
        new_label = []
        for i in self.labels:
            if i.dependency == type_:
                i.line = line
                self.resolvedLabels.append(i)
            else:
                new_label.append(i)
        self.labels = new_label

    def literalOrValue(self, value):
        if '"' in value:
            return self.add_code_for_latter('LIT', value, 0, False, None)

        if self.exists(value):
            return self.add_code_for_latter('LOD', value, 0, False, None)

        else:
            self.add_err('Accesing non existing variable', '', -1)




    def imprimenl(self, pila):
        message = ''
        lista = deque()
        pila.pop()
        first = 0
        lista.append(self.add_code_for_latter('OPR', 0, 21, False, None))
        while len(pila) > 0:
            nxt = pila.pop()
            if '"' in nxt:
                if first > 0:
                    lista.append(self.add_code_for_latter('OPR', 0, 20, False, None))
                first += 1
                lista.append(self.add_code_for_latter('LIT', nxt, 0, False, None)) # TAKE TO THE QUEUE OF COMPILER

            elif self.exists(nxt):
                search = self.search(nxt)
                if search.type == "F":
                    if first > 0:
                        lista.append(self.add_code_for_latter('OPR', 0, 20, False, None))
                    first += 1
                    lista.append(self.add_code_for_latter('LOD', nxt, 0, False, None))
                    lista.append(self.add_code_for_latter('CAL', nxt, 0, False, None))
                    nxt = pila.pop()
                    while nxt != 'PARAM':
                        if self.exists(nxt):
                            lista.append(self.add_code_for_latter('LOD', nxt, 0, False, None))

                        nxt = pila.pop()
                else:
                    if first > 0:
                        lista.append(self.add_code_for_latter('OPR', 0, 20, False, None))
                    first += 1
                    lista.append(self.add_code_for_latter('LOD', nxt, 0, False, None))
            else:
                if nxt == 'SEA':
                    pila.append('IMPRNL')
                    lista.append('///')
                    pila.append(nxt)
                    self.inner_sentences += lista
                    break
                if nxt not in self.estatutos:
                    self.add_err('Trying to print a non exiting value', nxt, -1)
                else:
                    pila.append(nxt)
                    pila.append('IMPRNL')
                    lista.append('///')
                    self.inner_sentences += lista
                    break



            if len(pila) == 0:
                self.take_everything_to_eje(lista)


    # OPCODE --> 19 its to read input from console
    def lee(self, pila):
        OPCODE = 19
        top = pila.pop()

        ident = pila.pop()
        if self.exists(ident):
            if self.search(ident).type != 'C':
                self.add_code('OPR', ident, OPCODE)
            else:
                self.add_err("Saving input from user to a constant", '', -1)
        else:
            self.add_err("Saving input from user of non existing variable", '[]', -1)

    # LOD --> Load values from the ones existing

    def opr_log(self, nxt):
        if nxt == 'O':
            return self.add_code_for_latter('OPR', 0, 15, False, None)
        elif nxt == 'Y':
            return self.add_code_for_latter('OPR', 0, 16, False, None)
        else:
            return self.add_code_for_latter('OPR', 0, 17, False, None)

    def opr_rel(self, nxt):
        if nxt == '<':
            # return self.add_code_for_latter('OPR', 0, 9)
            return self.add_code_for_latter('OPR', 0, 9, False, None)
        elif nxt == '>':
            # return self.add_code_for_latter('OPR', 0, 10)
            return self.add_code_for_latter('OPR', 0, 10, False, None)
        elif nxt == '<=':
            return self.add_code_for_latter('OPR', 0, 11, False, None)
        elif nxt == '>=':
            return self.add_code_for_latter('OPR', 0, 12, False, None)
        elif nxt == '<>':
            return self.add_code_for_latter('OPR', 0, 13, False, None)
        elif nxt == '=':
            return self.add_code_for_latter('OPR', 0, 14, False, None)

    def limpia(self):
        return self.add_code_for_latter('OPR', 0, 18, False, None)

    def if_statemen(self, pila):
        not_discard = None
        lista = deque()
        # First, we add the jump if the condition is false
        #lista.append(self.add_code_for_latter('JMC', 'F', 'E'+str(self.labelCont)))
        lista.append(self.add_code_for_latter('JMC', 'F', 'E' + str(self.labelCont), False, None))
        self.labelCont += 1
        while len(pila) > 0:
            nxt = pila.pop()
            if nxt in self.nexos:
                lista.append(self.opr_log(nxt))
            elif nxt in self.oprel:
                lista.append(self.opr_rel(nxt))
            elif nxt in self.estatutos:
                if nxt == 'IMPRNL':
                    not_discard = nxt
                else:
                    pila.append(nxt)
                    if not_discard is not None:
                        pila.append(not_discard)
                    return lista
            else:
                lista.append(self.literalOrValue(nxt))
        if not_discard is not None:
            pila.append(not_discard)
        return lista

    def statuto(self, pila, top):
        lista = deque()
        if top == 'SI':
            lista = self.if_statemen(pila)
        if top == 'LIMPIA':
            lista = self.limpia()
        if top == 'IMPRNL':
            lista = self.returnUntil(self.inner_sentences, '///')
        return lista

    def returnUntil(self, accum, char):
        accum.pop()
        nxt = ''
        actual = deque()
        while len(accum) > 0:
            nxt = accum.pop()
            if nxt == char:
                accum.append(char)
                break
            else:
                actual.appendleft(nxt)

        return actual

    def addTag(self, pila, tag):
        top = pila.pop()
        top.type = tag
        pila.append(top)
        top.istTag = True
        top.pendingTag = True

    def cuando(self, pila):
        final = deque()

        pila.pop()
        lod_usual = pila.pop()
        lod_usual = self.add_code_for_latter('LOD', lod_usual, 0, False, None)
        nxt = pila.pop()
        previousTag = None

        #final.append(self.add_code_for_latter('', '', '', True, 'FIN_CUANDO'))
        while len(pila) > 0:
            if nxt == 'OTRO':
                nxtTo = pila.pop()
                if nxtTo == 'SEA':
                    print("hhhhh")

                    nxt = pila.pop()
                    print(nxt)
                    pila.append('SEA')

                other = deque()
                other = self.statuto(pila, nxt)


                if len(pila) > 0:
                    nxt = pila.pop()
                if nxt == 'SEA':
                    self.addTag(other, 'SIGUIENTE_SEA')
                    final += other
                    continue
            elif nxt == 'SEA':
                print(pila)
                # Recover all block instruncitons
                nxt = pila.pop()
                other = deque()
                other.append(self.add_code_for_latter('JMP', 0, '_EF'+str(self.endCycleCont), False, 'DEP FIN_CUANDO'))
                if nxt == 'IMPRNL':
                    other += self.returnUntil(self.inner_sentences, '///')
                nxt = pila.pop()
                inicio = deque()
                self.addTag(other, 'INICIO_SEA')
                while len(pila) > 0:
                    print(pila)
                    if '"' in nxt:

                        inicio.appendleft(lod_usual)
                        inicio.appendleft(self.add_code_for_latter('LIT', nxt, 0, False, None))
                        inicio.appendleft(self.add_code_for_latter('OPR', 0, 14, False, None))
                        '''
                        inicio.appendleft(self.add_code_for_latter('LIT', nxt, 0))
                        inicio.appendleft(self.add_code_for_latter('OPR', 0, 14))'''

                        nextOne = pila.pop()

                        #inicio.appendleft(self.add_code_for_latter('JMC', 'V', 'E' + str(self.labelCont)))
                        inicio.appendleft(self.add_code_for_latter('JMC', 'V', '_E' + str(self.labelCont), True, 'DEP INICIO_SEA'))
                        if nextOne == '$$$':
                            self.labelCont += 1
                            # inicio.appendleft(self.add_code_for_latter('JMP', 0, 'E' + str(self.labelCont))
                            inicio.appendleft(self.add_code_for_latter('JMP', 0, '_E' + str(self.labelCont), True, 'DEP SIGUIENTE_SEA'))

                        pila.append(nextOne)

                    elif nxt == '$$$':
                        self.addTag(inicio, 'SIGUIENTE_SEA')
                        self.labelCont += 1
                        break
                    nxt = pila.pop()
                final += other
                final += inicio
                if len(pila) > 0:
                    nxt = pila.pop()
                elif len(pila) == 0:
                    break

        self.take_everything_to_eje(final)
        self.add_endTag()

    def add_endTag(self):
        print('_EF' + str(self.endCycleCont) + ',I' + ',I,' + str(self.cont), '0' + '#')


    def repetir(self, pila):
        top = pila.pop()
        nxt = pila.pop()
        lista = deque()
        lista.append(self.add_code_for_latter('JMC', 'F', 'E'+str(self.labelCont)))
        self.labelCont += 1
        while len(pila) > 0:
            if nxt in self.nexos:
                lista.append(self.opr_log(nxt))
                nxt = pila.pop()
            if nxt in self.oprel:
                lista.append(self.opr_rel(nxt))
                nxt = pila.pop()
            else:
                lista.append(self.literalOrValue(nxt))
                if len(pila) > 0:
                    nxt = pila.pop()

        self.take_everything_to_eje(lista)



    def add_err(self, lex_error, val, line):
        if line == -1:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + "\n")
        elif line == -2:
            self.err_file.write("err: " + lex_error + "\n")
        else:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")

    def add_code_for_latter(self, instruction, firstparam, secondparam, istTag, type_):
        return Instruction(instruction, firstparam, secondparam, istTag, type_)

    def add_code(self, instruction, firstparam, secondparam):
        self.instrucciones += str(self.cont) + ' ' + instruction + ' ' + str(firstparam) + ', ' + str(secondparam) + "\n"
        self.cont += 1
