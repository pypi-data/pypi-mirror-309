class Identifier:
    def __init__(self):
        self._identifier = None

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, rhs):
        self._identifier = rhs
