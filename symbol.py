class Nodo:
    def __init__(self):
        self.name = ""
        self.type = None
        self.datatype = None
        self.dimens = [0, 0]
        self.value = None
        self.dependency = dict()
        self.undefined = True
        self.scope = None



    def get_char(self):
        if isinstance(self.value, str):
            return ord(self.value)
        elif isinstance(self.value, int):
            return chr(self.value)
        return

class Instruction:
    def __init__(self, op, firstparam, secondparam, isStartBlock, type_):
        self.op = op
        self.param_1 = firstparam
        self.param_2 = secondparam
        self.pendingTag = False

        if isStartBlock:
            self.pendingTag = True
            self.istTag = True
        self.type = type_

    def changeToLabel(self, type_):
        if type_ is not None:
            self.type = type_
        self.pendingTag = True
        self.istTag = True





