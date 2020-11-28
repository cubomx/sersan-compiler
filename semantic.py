from symbol import Nodo
from collections import deque


class SymbolTable:
    def __init__(self, file, filename):
        self.estatutos = ('LIMPIA',
                     'SI', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'REGRESA', 'IMPRIME', 'IMPRIMENL', 'LEE',
                     'INTERRUMPE', 'CONTINUA', 'HACER', 'SINO', 'EL',
                     'VALOR', 'QUE', 'SE', 'CUMPLA', 'SEA', 'OTRO', 'IMPRNL')
        self.nexos = ('Y', 'O', 'NO')
        self.oprel = ('<>', '<=', '>=', '<', '>', '=')
        self.dict = dict()
        self.labels = dict()
        self.err_file = file
        self.file_name = filename
        open(self.file_name + ".eje", 'w').close()
        self.eje = open(self.file_name + ".eje", "a")
        self.cont = 1
        self.inner_sentences = deque()
        self.compareTO = ''

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
                self.add_err("Cannot redeclared const ", new_nodo.name, -2)
            else:
                self.dict[new_nodo.name] = new_nodo
            if len(pila) == 0:
                top = ''

    def add_to_table(self, new_nodo):
        if self.exists(new_nodo.name):
            self.add_err("Cannot redeclared variable ", new_nodo.name, -2)
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
        procNode = Nodo()
        procNode.name = pila.pop()
        procNode.type = 'P'
        procNode.datatype = 'I'
        self.add_to_table(procNode)

        type_ = pila.pop()
        upp_type = type_.upper()
        self.checkForParams(pila, upp_type, procNode)



    def is_valid_value(self, nxt, newNodo, dimension):
        if nxt.isdigit():
            print("hei33333333333333333333333")
            newNodo.dimens[dimension] = int(nxt)
        else:
            try:
                floating = float(nxt)
                self.add_err("Cannot use real number as index", nxt, -2)
            except ValueError:
                search = self.search(nxt)
                if search is not None:
                    if search.datatype == "E":
                        if search.value is not None:
                            newNodo.dimens[dimension] = search.value
                        else:
                            self.add_err("Declaring size of array of not initialized value", search.name, -2)
                    else:
                        self.add_err("Declaring size of array with non integer index", search.name, -2)
                else:
                    self.add_err("Declaring size of array of undefined value", nxt, -2)


    def var_add(self, pila):
        datatype = pila.pop()
        type_ = 'V'
        top = pila.pop()
        pila_matrices = deque()
        while True:
            print(pila)
            newNodo = Nodo()
            new_ = pila.pop()
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
            self.eje.write(str(self.cont) + ' ' + el)
            self.cont += 1

    def literalOrValue(self, value):
        if '"' in value:
            return self.add_code_for_latter('LIT', value, 0)

        if self.exists(value):
            return self.add_code_for_latter('LOD', value, 0)

        else:
            self.add_err('Accesing non existing variable', '', -1)




    def imprimenl(self, pila):
        message = ''
        lista = deque()
        pila.pop()
        first = 0
        lista.append(self.add_code_for_latter('OPR', 0, 21))
        while True:
            nxt = pila.pop()
            if '"' in nxt:
                if first > 0:
                    lista.append(self.add_code_for_latter('OPR', 0, 20))
                first += 1
                lista.append(self.add_code_for_latter('LIT', nxt, 0)) # TAKE TO THE QUEUE OF COMPILER

            elif self.exists(nxt):
                search = self.search(nxt)
                if search.type == "F":
                    if first > 0:
                        lista.append(self.add_code_for_latter('OPR', 0, 20))
                    first += 1
                    lista.append(self.add_code_for_latter('LOD', nxt, 0))
                    lista.append(self.add_code_for_latter('CAL', nxt, 0))
                    nxt = pila.pop()
                    while nxt != 'PARAM':
                        if self.exists(nxt):
                            lista.append(self.add_code_for_latter('LOD', nxt, 0))

                        nxt = pila.pop()
                else:
                    if first > 0:
                        lista.append(self.add_code_for_latter('OPR', 0, 20))
                    first += 1
                    lista.append(self.add_code_for_latter('LOD', nxt, 0 ))
            else:
                if nxt == 'SEA':
                    pila.append('IMPRNL')
                    pila.append(nxt)
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

    def if_statemen(self, pila):
        not_discard = None
        lista = deque()
        while len(pila) > 0:
            nxt = pila.pop()
            if nxt in self.nexos:
                if nxt == 'Y':
                    lista.append(self.add_code_for_latter('OPR', 0, 15))
                elif nxt == 'O':
                    lista.append(self.add_code_for_latter('OPR', 0, 16))
                else:
                    lista.append(self.add_code_for_latter('OPR', 0, 17))
            elif nxt in self.oprel:
                if nxt == '<':
                    lista.append(self.add_code_for_latter('OPR', 0, 9))
                elif nxt == '>':
                    lista.append(self.add_code_for_latter('OPR', 0, 10))
                elif nxt == '<=':
                    lista.append(self.add_code_for_latter('OPR', 0, 11))
                elif nxt == '>=':
                    lista.append(self.add_code_for_latter('OPR', 0, 12))
                elif nxt == '<>':
                    lista.append(self.add_code_for_latter('OPR', 0, 13))
                elif nxt == '=':
                    lista.append(self.add_code_for_latter('OPR', 0, 14))
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

    def statuto(self, pila):
        top = pila.pop()
        lista = deque()
        if top == 'SI':
            lista = self.if_statemen(pila)

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



    def cuando(self, pila):
        final = deque()

        pila.pop()
        lod_usual = pila.pop()
        lod_usual = self.add_code_for_latter('LOD', lod_usual, 0)

        nxt = pila.pop()
        while len(pila) > 0:
            if nxt == 'OTRO':
                other = None
                add = self.statuto(pila)
                print(pila)
                nxt = pila.pop()
                if nxt == 'IMPRNL':
                    other = self.returnUntil(self.inner_sentences, '///')
                    if len(add) > 0:
                        other += add
                nxt = pila.pop()
                print(pila)
                print(nxt)
                if nxt == 'SEA':
                    final += other
                    continue
            elif nxt == 'SEA':
                print("hhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                # Recover all block instruncitons
                nxt = pila.pop()
                other = deque()
                if nxt == 'IMPRNL':
                    other += self.returnUntil(self.inner_sentences, '///')
                nxt = pila.pop()
                print(nxt)
                while len(pila) > 0:
                    print(pila)
                    if '"' in nxt:
                        other.append(self.add_code_for_latter('OPR', 0, 14))
                        other.append(self.add_code_for_latter('LIT', nxt, 0))
                        other.append(lod_usual)
                    elif nxt == '$$$':
                        break
                    nxt = pila.pop()
                final += other
                if len(pila) > 0:
                    nxt = pila.pop()
                elif len(pila) == 0:
                    break
                print(pila)

        self.take_everything_to_eje(final)


    def sea_instruction(self, pila):
        top = pila.pop()
        cont = 0
        nxt = pila.pop()
        while len(pila) > 0 or nxt != '$$$':
            self.add_code('LIT')


    def add_err(self, lex_error, val, line):
        if line == -1:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + "\n")
        elif line == -2:
            self.err_file.write("err: " + lex_error + "\n")
        else:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")

    def add_code_for_latter(self, instruction, firstparam, secondparam):
        return instruction + ' ' + str(firstparam) + ', ' + str(secondparam) + "\n"

    def add_code(self, instruction, firstparam, secondparam):
        self.eje.write(str(self.cont) + ' ' + instruction + ' ' + str(firstparam) + ', ' + str(secondparam) + "\n")
        self.cont += 1