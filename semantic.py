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

    def __str__(self):
        string = ""
        for key, value in self.dict.items():
            string += key + ", " + value.type + ", " + value.datatype + ", " + str(value.dimens[0]) + ", " + str(value.dimens[1]) +", #," + "\n"

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
                newNodo.datatype = datatype
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








    def imprime(self, pila):
        return

    # OPCODE --> 19 its to read input from console
    def lee(self, pila):
        OPCODE = 19
        top = pila.pop()
        ident = pila.pop()
        self.add_code('OPR', ident, OPCODE)

    def gruposea(self, pila):
        return

    def add_err(self, lex_error, val, line):
        if line == -1:
            self.err_file.write("err: " + lex_error + + "[" + val + "]" + "\n")
        elif line == -2:
            self.err_file.write("err: " + lex_error + "\n")
        else:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")

    def add_code(self, instruction, firstparam, secondparam):
        self.eje.write(str(self.cont) + ' ' + instruction + ' ' + str(firstparam) + ', ' + str(secondparam) + "\n")
        self.cont+=1


