class DungeonProxy:
    def __init__(self, dungeon):
        self._dg = dungeon

    @property
    def width(self):
        return self._dg.width

    @property
    def height(self):
        return self._dg.height

    @property
    def cells(self):
        return self._dg.cells

    @property
    def rooms(self):
        return self._dg.rooms

    def in_bounds(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True
