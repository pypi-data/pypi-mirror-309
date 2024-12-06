from .dimensions import Dimensions
from .directions import Directions
from .position import Position


class Room(Dimensions, Position):
    def __init__(self, width, height):
        Dimensions.__init__(self, width, height)
        Position.__init__(self)

        self._identifier = None
        self._orig_identifier = None

    def set_position(self, x, y):
        self._x = x
        self._y = y

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, rhs):
        self._identifier = rhs
        if self._orig_identifier is None:
            self._orig_identifier = rhs

    def get_relative_corner(self, direction, i=None):
        """
        Get the "top left" corner, based on viewing the room
        from the given direction:
          NORTH = North West corner = real top left
          EAST  = North East corner = real top right
          SOUTH = South East corner = real bottom right
          WEST  = South West corner = real bottom left

        When i is passed, it takes precedence over the axis value of the direction
        """
        if direction == Directions.NORTH:
            if i is None:
                i = self.x
            return i, self.y
        if direction == Directions.EAST:
            if i is None:
                i = self.y
            return self.x + self.width - 1, i
        if direction == Directions.SOUTH:
            if i is None:
                i = self.x + self.width - 1
            return i, self.y + self.height - 1
        if direction == Directions.WEST:
            if i is None:
                i = self.y + self.height - 1
            return self.x, i
        return None, None  # pragma: no cover
