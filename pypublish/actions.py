class BaseAction:
    def __init__(self):
        pass

    def accept(self, block):
        if 'action' not in block.keys():
            raise SyntaxError("No 'action' defined")
        return self.key() == block['action']

    def key(self):
        raise NotImplementedError


class DeriveFromSourceAction(BaseAction):
    def __init__(self):
        BaseAction.__init__(self)
        print "__init__ of DeriveFromSourceAction"

    def process(self, block):
        print "Process"
        return True

    def key(self):
        return "derive from source file"
