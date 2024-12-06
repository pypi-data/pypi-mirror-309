from . import constants as C
from .cell import Cell
from .dimensions import Dimensions


# pylint: disable=protected-access
class IDungeon:
    def __init__(self, dungeon):
        self._dg = dungeon

    @property
    def args(self):
        return self._dg._args

    @property
    def dungeon(self):
        return self._dg

    @property
    def width(self):
        return self._dg.width

    @property
    def height(self):
        return self._dg.height

    @property
    def area(self):
        return self.height * self.width

    @property
    def room_tree(self):
        return self._dg._room_tree

    def set_room_tree(self, tree):
        self._dg._room_tree = tree

    @property
    def deadends(self):
        return self._dg._deadends

    def add_deadend(self, cell):
        self._dg._deadends += [cell]

    def set_deadends(self, cells):
        self._dg._deadends = cells

    def loop_xy(self):
        """
        Return a tuples of (x,y) tuples with the coordinates of
        the room.
        Equivalent to:
        for x in range(0, self.width):
          for y in range(0, self.height):
            x = x + room.x
            y = y + room.y
        """
        yield from ((x, y) for x in range(0, self.width) for y in range(0, self.height))

    def loop_cells(self):
        yield from (self.cells[x][y] for x, y in self.loop_xy())

    @property
    def cells(self):
        return self._dg._cells

    @property
    def rooms(self):
        return self._dg._rooms

    def add_room(self, room):
        """
        Add room to map if it does not overlap with anything
        Return True if added
        """
        # Verify placement
        for x, y in room.loop_xy():
            cell = self.cells[x][y]
            if not cell.is_empty():
                return False

        # Give the room an identifier (base 1)
        self._dg._rooms += [room]
        return self.set_room(room, len(self.rooms))

    def set_room(self, room, identifier):
        # For every cell contained by this room, set the identifier
        room.identifier = identifier
        room.set_center_cell(self.cells)
        for x, y in room.loop_xy():
            cell = self.cells[x][y]
            cell.set_room(identifier)
        return True

    def order_rooms(self):
        """
        Order rooms so that top left room is 1, etc.
        """
        # Set all identifiers to negative
        for room in self.rooms:
            self.set_room(room, room.identifier * -1)

        # Once sorted, distribute the new identifiers
        self._dg._rooms = sorted(self.rooms)
        for index, room in zip(range(len(self._dg._rooms)), self._dg._rooms):
            self.set_room(room, index + 1)

    def minimize_identifiers(self, identifiers):
        """
        Loop through all the cells.
        If the identifier is in the param "identifier" list,
        then set the identifier to the smallest value from that list

        When all cell identifiers are None or 1, then the map is all
        connected.
        """
        min_id = min(identifiers)

        cells = [cell for cell in self.loop_cells() if cell.identifier in identifiers]
        for cell in cells:
            cell.identifier = min_id

    def get_adjacent(self, cell, direction):
        x = cell.x + C.DIRECTIONS_X[direction]
        y = cell.y + C.DIRECTIONS_Y[direction]
        if x < 0 or y < 0:
            return None
        if x >= self.width or y >= self.height:
            return None
        return self.cells[x][y]

    def get_bordering_cells(self, cell):
        n_cell = self.get_adjacent(cell, C.Directions.NORTH)
        e_cell = self.get_adjacent(cell, C.Directions.EAST)
        s_cell = self.get_adjacent(cell, C.Directions.SOUTH)
        w_cell = self.get_adjacent(cell, C.Directions.WEST)
        return n_cell, e_cell, s_cell, w_cell


class Dungeon(Dimensions, IDungeon):
    def __init__(self, args):
        IDungeon.__init__(self, self)
        Dimensions.__init__(self, args["map_width"], args["map_height"])

        # Keep a copy of arguments
        self._args = args

        # List of rooms
        self._rooms = []

        # List of rooms that are connected to another
        self._room_tree = []

        # List of cells that are deadends
        self._deadends = []

        # Create cells
        def index(x, y):
            return (self.height - y - 1) * self.width + x

        self._cells = [[Cell(x, y, index(x, y)) for y in range(self.height)] for x in range(self.width)]
