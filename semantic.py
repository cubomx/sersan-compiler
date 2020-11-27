from symbol import Nodo
from collections import deque


class SymbolTable:
    def __init__(self, file, filename):
        self.dict = dict()
        self.err_file = file
        self.file_name = filename
        open(self.file_name + ".eje", 'w').close()
        self.eje = open(self.file_name + ".eje", "a")
        self.cont = 1
        self.inner_sentences = deque()

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

    def imprimenl(self, pila):
        message = ''
        lista = deque()
        pila.pop()
        nxt = pila.pop()

        if '"' in nxt:
            #self.add_code_for_latter()
            return
        elif self.exists(nxt):
            search = self.search(nxt)
            if search.type == "F":
                return
            else:
                return


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

    def gruposea(self, pila):
        # We need the value of the ident
        pila.pop()
        ident = pila.pop()
        if self.exists(ident):
            pila.pop()
            while True:
                self.add_code('LOD', ident, 0)
                literal = pila.pop()
                if literal == '$$$':
                    break
                if literal.isalpha():
                    self.add_code('LIT', literal, 0)


        else:
            self.add_err("Trying to access a non existent value", '', -1)
        return



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


