from enum import Enum

from .identifier import Identifier
from .position import Position


class FloorType(Enum):
    EMPTY = 0
    ROOM = 1
    CORRIDOR = 2


class Cell(Position, Identifier):
    def __init__(self, x, y, index=None):
        Position.__init__(self, x, y)
        Identifier.__init__(self)

        # The NWN tile index
        self._index = index

        # Cell favored direction, used when tunneling
        self._direction = None

        # All cells start as empty, and are then filled
        self._floor_type = FloorType.EMPTY

        # Room identifier is set once
        self._room_identifier = None

    def __repr__(self):
        retval = {
            "x": self.x,
            "y": self.y,
            "index": self.index,
            "identifier": self.identifier,
            "direction": self.direction,
        }
        return str(retval)

    def __lt__(self, rhs):
        if self.x < rhs.x:
            return True
        if self.x > rhs.x:
            return False
        if self.y < rhs.y:
            return True
        return False

    @property
    def index(self):
        return self._index

    @property
    def key(self):
        return {
            FloorType.EMPTY: "W",
            FloorType.ROOM: "R",
            FloorType.CORRIDOR: "C",
        }[self._floor_type]

    @property
    def room_identifier(self):
        return self._room_identifier

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, rhs):
        self._direction = rhs

    def is_empty(self):
        return self._floor_type not in [FloorType.ROOM, FloorType.CORRIDOR]

    def is_room(self):
        return self._floor_type == FloorType.ROOM

    def is_corridor(self):
        return self._floor_type == FloorType.CORRIDOR

    def is_open(self):
        return self._floor_type in [FloorType.CORRIDOR, FloorType.ROOM]

    def set_room(self, identifier):
        self._identifier = identifier
        self._room_identifier = identifier
        self._floor_type = FloorType.ROOM

    def set_corridor(self, identifier, direction=None):
        self._floor_type = FloorType.CORRIDOR
        self._identifier = identifier
        self._direction = direction

    def clear(self):
        self._identifier = None
        self._room_identifier = None
        self._floor_type = FloorType.EMPTY
