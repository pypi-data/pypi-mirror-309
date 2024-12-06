class Position:
    def __init__(self, x=None, y=None):
        self._x = x
        self._y = y

    def __lt__(self, rhs):
        # We sort from top-left to bottom-right
        if self.y < rhs.y:
            return True
        if self.y > rhs.y:
            return False
        if self.x < rhs.x:
            return True
        return False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
