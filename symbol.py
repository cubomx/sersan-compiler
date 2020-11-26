class Nodo:
    def __init__(self):
        self.name = ""
        self.type = None
        self.datatype = None
        self.dimens = [0, 0]
        self.value = None
        self.dependency = None
        self.undefined = True


    def get_char(self):
        if isinstance(self.value, str):
            return ord(self.value)
        elif isinstance(self.value, int):
            return chr(self.value)
        return

