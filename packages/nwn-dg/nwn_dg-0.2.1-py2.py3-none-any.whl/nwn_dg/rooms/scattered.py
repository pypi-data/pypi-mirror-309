import random

from .. import constants as C
from ..dungeon import IDungeon
from ..room import Room

ROOM_WIDTH = 3
ROOM_HEIGHT = 3
TENTATIVES = 10


class Scattered(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

    def generate(self):
        map_max_rooms = self.args.get("map_max_rooms")
        map_min_rooms = self.args.get("map_min_rooms", C.DEFAULT_MAP_MIN_ROOMS)
        map_room_ratio = self.args.get("map_room_ratio", C.DEFAULT_MAP_ROOM_RATIO)

        # Add one to account to bordering empty cells
        room_area = (ROOM_WIDTH + 1) * (ROOM_HEIGHT + 1)
        max_rooms = self.area // room_area

        max_rooms = max_rooms * map_room_ratio // 100
        max_rooms = max(max_rooms, 1)
        if map_max_rooms and max_rooms > map_max_rooms:
            max_rooms = map_max_rooms

        for _ in range(max_rooms):
            room = Room(ROOM_WIDTH, ROOM_HEIGHT)
            self._place_room(room)

        if len(self.rooms) < map_min_rooms:
            raise SystemExit(f"error: Failed to create a minimum of {map_min_rooms} rooms")

        self.order_rooms()

    def _place_room(self, room):
        tentatives = TENTATIVES

        while tentatives > 0:
            tentatives -= 1

            # Find a random place, and try to place it
            x = (random.randint(0, self.width - room.width) // 2) * 2
            y = (random.randint(0, self.height - room.height) // 2) * 2

            room.set_position(x, y)
            if self.add_room(room):
                return
