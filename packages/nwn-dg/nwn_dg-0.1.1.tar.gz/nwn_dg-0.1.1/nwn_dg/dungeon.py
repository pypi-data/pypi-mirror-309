from .cell import Cell
from .dimensions import Dimensions


class Dungeon(Dimensions):
    def __init__(self, args):
        Dimensions.__init__(self, args["map_width"], args["map_height"])

        self._filepath = args["filepath"]

        # List of rooms
        self._rooms = []

        # Create cells
        self._cells = []
        self._init_cells()

    @property
    def cells(self):
        return self._cells

    @property
    def rooms(self):
        return self._rooms

    def _init_cells(self):
        w = self._width
        h = self._height
        self._cells = [[Cell(x, y) for y in range(h)] for x in range(w)]

    def add_room(self, room):
        """
        Add room to map if it does not overlap with anything
        Return True if added
        """
        # Verify placement
        for x in range(room.width):
            for y in range(room.height):
                cell = self.cells[x + room.x][y + room.y]
                if not cell.is_empty():
                    return False

        # Give the room an identifier (base 1)
        self._rooms += [room]
        room.identifier = len(self._rooms)

        # For every cell contained by this room, set the identifier
        for x in range(room.width):
            for y in range(room.height):
                cell = self.cells[x + room.x][y + room.y]
                cell.set_room(room.identifier)
        return True

    def del_room(self, room_id):
        self._rooms = [room for room in self._rooms if room.identifier != room_id]

    def walk_rooms(self):
        yield from self._rooms

    def merge_identifiers(self, identifiers):
        min_id = min(identifiers)

        for room in self.walk_rooms():
            if room.identifier in identifiers:
                room.identifier = min_id

        for x in range(self.width):
            for y in range(self.height):
                cell = self._cells[x][y]
                if cell.identifier in identifiers:
                    cell.identifier = min_id
