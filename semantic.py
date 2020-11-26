from symbol import Nodo

class symbolTable:
    def __init__(self, file):
        self.dict = dict()
        self.err_file = file

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

    def add_err(self, lex_error, val, line):
        if line == -1:
            self.err_file.write("err: " + lex_error + + "[" + val + "]" + "\n")
        elif line == -2:
            self.err_file.write("err: " + lex_error + "\n")
        else:
            self.err_file.write("err: " + lex_error + "[" + val + "]" + " in line " + str(line) + "\n")


