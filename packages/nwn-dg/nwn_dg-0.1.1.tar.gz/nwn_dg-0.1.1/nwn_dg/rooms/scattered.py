import random

from ..proxy import DungeonProxy
from ..room import Room

ROOM_WIDTH = 3
ROOM_HEIGHT = 3


class Scattered(DungeonProxy):
    def __init__(self, dungeon, args):
        DungeonProxy.__init__(self, dungeon)
        self._map_min_rooms = args.get("map_min_rooms", 1)
        self._map_max_rooms = args.get("map_max_rooms")
        self._map_room_ratio = args.get("map_room_ratio", 100)

    # TODO: Enable different methods for room generation: scattered, packed, bsp, ...
    def create_rooms(self):
        room_area = ROOM_WIDTH * ROOM_HEIGHT
        map_area = self.width * self.height
        max_rooms = map_area // room_area // 2

        max_rooms = max_rooms * self._map_room_ratio // 100
        max_rooms = max(max_rooms, 1)

        if self._map_max_rooms and max_rooms > self._map_max_rooms:
            max_rooms = self._map_max_rooms

        for _ in range(max_rooms):
            room = Room(3, 3)
            self.emplace_room(room)

        if len(self.rooms) < self._map_min_rooms:
            raise SystemExit(f"error: Failed to create a minimum of {self._map_min_rooms} rooms")

    def emplace_room(self, room):
        tentatives = 10
        while tentatives > 0:
            # Find a random place, and try to place it
            x = (random.randint(0, self.width - room.width) // 2) * 2
            y = (random.randint(0, self.height - room.height) // 2) * 2
            room.set_position(x, y)

            tentatives -= 1
            if self._dg.add_room(room):
                return
