"""
A sparse dungeon generates the rooms and corridors only on odd numbered cells.

Other online dungeon generators that use this method: https://donjon.bin.sh/d20/dungeon/ or https://www.d20srd.org/d20/dungeon/index.cgi

It's fine for most usage, but has the inconvenient of more "wasted" space in Neverwinter Nights.
"""

import copy
import math
import random

from ..directions import DIRECTIONS, Directions, get_clockwise, get_counterclockwise, get_new_position
from ..proxy import DungeonProxy
from ..rooms import Scattered


class Sparse(DungeonProxy):
    def __init__(self, dungeon, args):
        DungeonProxy.__init__(self, dungeon)
        if not (self.width & 1 and self.height & 1):
            raise SystemExit("error: dungeon width and height must both be odd numbers")

        self._map_bend_pct = args.get("map_bend_pct", 50)
        self._map_deadends_pct = args.get("map_deadends_pct", 50)
        self._map_reshape_pct = args.get("map_reshape_pct", 70)

        room_generator = Scattered(dungeon, args)
        room_generator.create_rooms()

        # List of cells to tunnel
        self._open_cells = []

        # List of all possible sills
        self._sills = []
        self.open_sills()

        # Deadends list are possible deadends, not necessarily deadends
        self._probable_deadends = []
        self.tunnel_all()

        # Some rooms might not be reachable, open new tunnels
        self.fix_unaccessible()

        # Remove some deadends
        self._deadends = []
        self.remove_deadends()

        # Reshape some rooms
        self.reshape_rooms()

    def open_sills(self):
        def get_openings_count(room):
            room_h = int((room.height / 2) + 1)
            room_w = int((room.width / 2) + 1)
            return max(int(math.sqrt(room_h * room_w)), 1)

        def is_possible_sill(room, x, y, direction):
            x, y = get_new_position(room.x + x, room.y + y, direction)
            cell = self.cells[x][y]
            if cell.is_empty() and cell not in self._sills:
                cell.direction = direction
                return cell
            return None

        def get_sills(room):
            sills = []
            if room.x >= 2:  # West border
                for y in range(0, room.height, 2):
                    sills += [is_possible_sill(room, 0, y, Directions.WEST)]
            if room.y >= 2:  # North border
                for x in range(0, room.width, 2):
                    sills += [is_possible_sill(room, x, 0, Directions.NORTH)]
            if room.x <= (self.width - room.width - 1):  # East border
                for y in range(0, room.height, 2):
                    sills += [is_possible_sill(room, room.width - 1, y, Directions.EAST)]
            if room.y <= (self.height - room.height - 1):  # South border
                for x in range(0, room.width, 2):
                    sills += [is_possible_sill(room, x, room.height - 1, Directions.SOUTH)]
            sills = [sill for sill in sills if sill is not None]
            return sills

        # Build a list of all rooms and sills, marking cells as sills
        for room in self._dg.walk_rooms():
            # Get the real sills, and get optional openings
            sills = get_sills(room)
            self._sills += sills

            # n_opens can be 0 because len(sills) is 0, which means room will probably end up
            # unaccessible. room will be opened later with the fix_unaccessible function
            n_opens = get_openings_count(room)
            n_opens = min(n_opens, len(sills))

            random.shuffle(sills)
            for _ in range(n_opens):
                sill = sills.pop(0)

                # When opening sills, open to the next odd cell
                x2, y2 = get_new_position(sill.x, sill.y, sill.direction)
                cell1 = self.cells[sill.x][sill.y]
                cell2 = self.cells[x2][y2]

                # cell1 (a sill) and cell2 reach out into the open
                if cell2.is_empty():
                    cell1.set_corridor(room.identifier, None)
                    cell2.set_corridor(room.identifier, sill.direction)
                    self._open_cells += [cell2]
                    continue

                # cell1 (a sill) connects to a room or an already open corridor
                if cell2.is_room() or cell2.is_corridor():
                    cell1.set_corridor(room.identifier, None)
                    self._dg.merge_identifiers([cell1.identifier, cell2.identifier])

                    # cell1 (a sill) connects to cell2 (a corridor)
                    if cell2.is_corridor():
                        self._open_cells += [cell2]
                    continue

    def tunnel_all(self):
        while len(self._open_cells) > 0:
            self.tunnel()

    def tunnel(self):
        def get_directions(last_dir):
            retval = copy.deepcopy(DIRECTIONS)
            random.shuffle(retval)
            if random.randint(1, 100) <= self._map_bend_pct and last_dir:
                retval.insert(0, last_dir)
            return retval

        def set_corridors(cell1, cell2, cell3=None):
            cell2.set_corridor(cell1.identifier, direction)
            self._open_cells += [cell1]
            if cell3:
                cell3.set_corridor(cell1.identifier, direction)
                self._open_cells += [cell3]

        if len(self._open_cells) == 0:
            return

        self._open_cells = sorted(list(set(self._open_cells)))
        random.shuffle(self._open_cells)
        cell1 = self._open_cells.pop(0)

        x1 = cell1.x
        y1 = cell1.y
        directions = get_directions(cell1.direction)
        for direction in directions:
            x2, y2 = get_new_position(x1, y1, direction)
            x3, y3 = get_new_position(x2, y2, direction)

            if not self.in_bounds(x2, y2):
                continue
            if not self.in_bounds(x3, y3):
                continue

            cell2 = self.cells[x2][y2]
            cell3 = self.cells[x3][y3]

            if not cell2.is_empty():
                continue

            # If we land on an empty space, then it's OK
            if cell3.is_empty():
                set_corridors(cell1, cell2, cell3)
                return
            if cell3.is_corridor():
                if cell1.identifier == cell3.identifier:
                    continue
                id1 = cell1.identifier
                id3 = cell3.identifier
                set_corridors(cell1, cell2, cell3)
                self._dg.merge_identifiers([id1, id3])
                return
            if cell3.is_room():
                if cell1.identifier == cell3.identifier:
                    continue
                # This opens a new sill
                id1 = cell1.identifier
                id3 = cell3.identifier
                set_corridors(cell1, cell2)
                self._dg.merge_identifiers([id1, id3])
                self._sills += [cell2]
                return
        # We didn't exit loop, so it's a possible deadend
        self._probable_deadends += [cell1]

    def fix_unaccessible(self):
        tentatives = 15
        while tentatives > 0:
            tentatives -= 1

            un_cells = []
            # List of unaccessible cells
            for x in range(self.width):
                for y in range(self.height):
                    cell = self.cells[x][y]
                    if cell.identifier not in [None, 1]:
                        un_cells += [cell]

            if len(un_cells) == 0:
                return

            # Open one tunnel from room ignored sills
            for cell in un_cells:
                # Ignore cells on even cells
                if cell.x & 1:
                    continue
                if cell.y & 1:
                    continue
                self._open_cells += [cell]
                self.tunnel()

        raise SystemExit("error: failed to solve all unaccessible areas")

    def remove_deadends(self):
        def get_exits(cell):
            exits = []
            for direction in DIRECTIONS:
                x, y = get_new_position(cell.x, cell.y, direction)
                if x < 0 or y < 0:
                    continue
                if x >= self.width or y >= self.height:
                    continue
                if not self.cells[x][y].is_empty():
                    exits += [self.cells[x][y]]
            return exits

        # Reduce possible deadends to real deadends
        self._probable_deadends = sorted(list(set(self._probable_deadends)))
        for cell in self._probable_deadends:
            if cell.is_empty():
                continue
            if len(get_exits(cell)) <= 1:
                self._deadends += [cell]
                cell._deadend = True

        if len(self._deadends) == 0:
            return

        pct = self._map_deadends_pct / 100
        k = int(len(self._deadends) * (1.0 - min(max(float(pct), 0.0), 1.0)))
        k = min(max(0, k), len(self._deadends))

        # deadends to remove, and deadends that remain
        rm_deadends = random.sample(self._deadends, k)
        self._deadends = [item for item in self._deadends if item not in rm_deadends]

        # Delete deadends
        while len(rm_deadends):
            cell = rm_deadends.pop(0)
            exits = get_exits(cell)
            if len(exits) <= 1:
                self.cells[cell.x][cell.y].clear()
                rm_deadends += exits

    def reshape_rooms(self):
        """
        For every room, check that the top is free of cells.
        For testing, imagine looking at a room and the top is at the top, then
        for the next test, "rotate" your head as if the new top is the right side
        """

        def get_range(room, direction, offset):
            if direction in [Directions.NORTH, Directions.SOUTH]:
                return range(room.x - offset, room.x + room.width + offset)
            if direction in [Directions.EAST, Directions.WEST]:
                return range(room.y - offset, room.y + room.height + offset)
            return None  # pragma: no cover

        def is_not_removable(x, y):
            return self.in_bounds(x, y) and not self.cells[x][y].is_empty()

        def is_reshape_dir(room, direction):
            left = get_counterclockwise(direction)
            right = get_clockwise(direction)

            # i can be x, y
            for i in get_range(room, direction, 1):
                x, y = room.get_relative_corner(direction, i)
                x, y = get_new_position(x, y, direction)
                if is_not_removable(x, y):
                    return None

            # The following is only valid for rooms of 3x3.
            # We passing to 5x5, we need to check several rows
            x, y = room.get_relative_corner(direction)
            x, y = get_new_position(x, y, left)
            if is_not_removable(x, y):
                return None

            x, y = room.get_relative_corner(get_clockwise(direction))
            x, y = get_new_position(x, y, right)
            if is_not_removable(x, y):
                return None
            return direction

        if not self._map_reshape_pct:
            return

        for room in self._dg.walk_rooms():
            reshape_dirs = []
            for direction in Directions:
                reshape_dirs += [is_reshape_dir(room, direction)]

            reshape_dirs = [x for x in reshape_dirs if x is not None]
            if not reshape_dirs:
                continue

            # We don't change the size of the room object as it's
            # no longer used.
            random.shuffle(reshape_dirs)
            for direction in reshape_dirs:
                if random.randint(1, 100) > self._map_reshape_pct:
                    continue
                for i in get_range(room, direction, 0):
                    x, y = room.get_relative_corner(direction, i)
                    if self.in_bounds(x, y):
                        self.cells[x][y].clear()
