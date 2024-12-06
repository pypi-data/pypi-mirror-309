"""
A sparse dungeon generates the rooms and corridors only on odd numbered cells.

Other online dungeon generators that use this method: https://donjon.bin.sh/d20/dungeon/ or https://www.d20srd.org/d20/dungeon/index.cgi

It's fine for most usage, but has the inconvenient of more "wasted" space in Neverwinter Nights.
"""

import itertools
import math
import random

from .. import constants as C
from ..dungeon import IDungeon
from ..rooms import Scattered


class Sparse(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)
        if not (self.width & 1 and self.height & 1):
            raise SystemExit("error: dungeon width and height must both be odd numbers")

        # List of cells to tunnel
        self._open_cells = []

    def generate(self):
        # Use the scattered room generator
        Scattered(self.dungeon).generate()

        # Cells that need to be tunneled. Build during _open_sills,
        # then used afterwards
        self._open_sills()

        # Deadends list are possible deadends, not necessarily deadends
        self._tunnel()

        # Some rooms might not be reachable, open new tunnels
        self._fix_unaccessible()

        # Remove some deadends
        self._remove_deadends()

        # Reshape some rooms
        self._reshape_rooms()

        # Calculate which rooms are connected to other rooms
        self._generate_room_tree()

    def _add_open_cell(self, cell):
        """
        Add a cell to be tunneled
        """
        self._open_cells += [cell]

    def _get_open_cell(self):
        self._open_cells = sorted(list(set(self._open_cells)))
        random.shuffle(self._open_cells)
        return self._open_cells.pop(0)

    def _get_cell_exits(self, cell):
        retval = []
        for direction in C.DIRECTIONS:
            n_cell = self.get_adjacent(cell, direction)
            if n_cell and n_cell.is_open():
                retval += [n_cell]
        return retval

    def _get_room_sills(self, room):
        def sill(x, y, direction):
            cell = self.cells[x][y]
            cell = self.get_adjacent(cell, direction)
            if cell is None or not cell.is_empty():
                return None
            cell.direction = direction
            return cell

        retval = []
        retval += [(room.x + x, room.y, C.Directions.NORTH) for x in range(0, room.width, 2)]
        retval += [(room.x + x, room.y + room.height - 1, C.Directions.SOUTH) for x in range(0, room.width, 2)]
        retval += [(room.x + room.height - 1, room.y + y, C.Directions.EAST) for y in range(0, room.height, 2)]
        retval += [(room.x, room.y + y, C.Directions.WEST) for y in range(0, room.height, 2)]

        retval = [(sill(x, y, direction)) for x, y, direction in retval]
        retval = [cell for cell in retval if cell is not None]
        return retval

    def _open_sills(self):
        """
        Sills are corridors that open from a room into the dungeon.
        They're placed on every other cell, and have
        one or two possible directions (ie: corners)
        """

        def get_openings_count(room):
            room_h = int((room.height / 2) + 1)
            room_w = int((room.width / 2) + 1)
            return max(int(math.sqrt(room_h * room_w)), 1)

        # ---
        #
        # For every room, build a list of sills
        # Open a random amount of sills per room, never opening or considering
        # a sill from another room
        sills = []
        for room in self.rooms:
            room_sills = [cell for cell in self._get_room_sills(room) if cell not in sills]
            sills += room_sills

            # n_opens can be 0 because len(sills) is 0, which means room will probably end up
            # unaccessible. room will be opened later with the fix_unaccessible function
            n_opens = get_openings_count(room)
            n_opens = min(n_opens, len(room_sills))

            random.shuffle(room_sills)
            for _ in range(n_opens):
                # The identifier evolves, so we must get it for every n_opens
                id1 = room.center.identifier

                cell2 = room_sills.pop(0)

                # When opening sills, open to the next odd cell
                cell3 = self.get_adjacent(cell2, cell2.direction)

                # cell2 (a sill) and cell3 reach out into the open
                if cell3.is_empty():
                    cell2.set_corridor(id1)
                    cell3.set_corridor(id1, cell2.direction)
                    self._add_open_cell(cell3)
                    continue

                # cell2 (a sill) connects to a room or an already open corridor
                if cell3.is_open():
                    cell2.set_corridor(id1)
                    self.minimize_identifiers([id1, cell3.identifier])

                    # cell2 (a sill) connects to cell3 (a corridor)
                    if cell3.is_corridor():
                        self._add_open_cell(cell3)
                    continue

    def _tunnel(self):
        while self._open_cells:
            self._tunnel_cell(False)

    def _tunnel_cell(self, open_room=False):
        """
        If open_room is True, then we can tunnel into a room and open
        a new sill
        """

        def set_corridors(direction, cell1, cell2, cell3=None):
            self._add_open_cell(cell1)
            cell2.set_corridor(cell1.identifier)
            if cell3:
                cell3.set_corridor(cell1.identifier, direction)
                self._add_open_cell(cell3)

        def get_random_directions(last_dir=None):
            """
            Return all four directions, with a priority on the last
            direction the cell was
            """
            map_bend_pct = self.args.get("map_bend_pct", C.DEFAULT_MAP_BEND_PCT)

            retval = list(C.DIRECTIONS)
            random.shuffle(retval)
            if not (random.randint(1, 100) <= map_bend_pct) and last_dir:
                retval.insert(0, last_dir)
            return retval

        # ---
        #
        if not self._open_cells:
            return

        cell1 = self._get_open_cell()
        directions = get_random_directions(cell1.direction)
        for direction in directions:
            cell2 = self.get_adjacent(cell1, direction)
            if cell2 is None or not cell2.is_empty():
                continue

            cell3 = self.get_adjacent(cell2, direction)
            if cell3 is None:
                continue
            # If we land on an empty space, then it's OK
            if cell3.is_empty():
                set_corridors(direction, cell1, cell2, cell3)
                return
            if cell3.is_corridor() or (open_room and cell3.is_room()):
                if cell1.identifier == cell3.identifier:
                    continue
                id1 = cell1.identifier
                id3 = cell3.identifier
                if cell3.is_corridor():
                    set_corridors(direction, cell1, cell2, cell3)
                else:
                    set_corridors(direction, cell1, cell2)
                self.minimize_identifiers([id1, id3])
                return

        # We didn't exit loop with a return, so it's a possible deadend
        exits = self._get_cell_exits(cell1)
        if len(exits) == 1:
            self.add_deadend(cell1)

    def _fix_unaccessible(self):
        def get_cells(x):
            return [cell for cell in x if cell.identifier not in [None, 1]]

        cells = get_cells(self.loop_cells())
        if not cells:
            return

        # Reduce to every other cell to keep corridors aligned
        cells = [cell for cell in cells if not (cell.x & 1 or cell.y & 1)]

        while cells:
            # Open any tunnel, even into a room
            self._open_cells += random.sample(cells, 1)
            self._tunnel_cell(True)
            cells = get_cells(cells)

    def _remove_deadends(self):
        if not self.deadends:
            return

        map_deadends_pct = self.args.get("map_deadends_pct", C.DEFAULT_MAP_DEADENDS_PCT)
        pct = map_deadends_pct / 100
        k = int(len(self.deadends) * (1.0 - min(max(float(pct), 0.0), 1.0)))
        k = min(max(0, k), len(self.deadends))

        # deadends to remove, and self.deadends that remain
        deadends = random.sample(self.deadends, k)
        self.set_deadends([i for i in self.deadends if i not in deadends])

        # Delete deadends
        while deadends:
            cell = deadends.pop(0)
            exits = self._get_cell_exits(cell)
            if len(exits) == 1:
                cell.clear()
                deadends += exits

    def _reshape_rooms(self):
        """
        For every room, check that the top is free of cells.
        For testing, imagine looking at a room and the top is at the top, then
        for the next test, "rotate" your head as if the new top is the right side
        """
        map_reshape_pct = self.args.get("map_reshape_pct", C.DEFAULT_MAP_RESHAPE_PCT)
        if not map_reshape_pct:
            return

        for room in self.rooms:
            # To remove a row or column from a room we need
            # to have as many sills as half the length, plus the two corners
            h_req_free = 2 + (room.width + 1) // 2
            v_req_free = 2 + (room.height + 1) // 2

            sills = self._get_room_sills(room)
            n_sills = [sill for sill in sills if sill.y <= room.north]
            e_sills = [sill for sill in sills if sill.x >= room.east]
            s_sills = [sill for sill in sills if sill.y >= room.south]
            w_sills = [sill for sill in sills if sill.x <= room.west]

            directions = []
            if len(n_sills) >= h_req_free:
                directions += [C.Directions.NORTH]
            if len(e_sills) >= v_req_free:
                directions += [C.Directions.EAST]
            if len(s_sills) >= h_req_free:
                directions += [C.Directions.SOUTH]
            if len(w_sills) >= v_req_free:
                directions += [C.Directions.WEST]
            if not directions:
                continue

            # We don't change the size of the room object as it's
            # no longer used.
            random.shuffle(directions)
            for direction in directions:
                # pylint: disable=superfluous-parens
                if not (random.randint(1, 100) <= map_reshape_pct):
                    continue
                if direction == C.Directions.NORTH:
                    for x in range(room.west, room.east + 1):
                        self.cells[x][room.north].clear()
                if direction == C.Directions.EAST:
                    for y in range(room.north, room.south + 1):
                        self.cells[room.east][y].clear()
                if direction == C.Directions.SOUTH:
                    for x in range(room.west, room.east + 1):
                        self.cells[x][room.south].clear()
                if direction == C.Directions.WEST:
                    for y in range(room.north, room.south + 1):
                        self.cells[room.west][y].clear()

    def _generate_room_tree(self):
        # For every room, do a dijkstra search for with all adjacent rooms
        result = [self._get_room_connections(room) for room in self.rooms]
        result = list(itertools.chain.from_iterable(result))
        result = list({(x[0], x[1]) for x in result})
        result = sorted(result)
        self.set_room_tree(result)

    def _get_room_connections(self, room):
        # Do a dijkstra search from the room center to all other
        # rooms that are connected.
        # Stop at empty cells, and at any new room
        open_cells = [room.center]
        closed_cells = []
        retval = []

        while open_cells:
            current = open_cells.pop()
            closed_cells += [current]
            for direction in C.DIRECTIONS:
                cell = self.get_adjacent(current, direction)
                if cell is None or cell.is_empty():
                    continue
                if cell in closed_cells or cell in open_cells:
                    continue
                if cell.room_identifier and cell.room_identifier != room.identifier:
                    pair = sorted([cell.room_identifier, room.identifier])
                    if pair not in retval:
                        retval += [pair]
                    # Don't explore the cell
                    closed_cells += [cell]
                    continue
                open_cells += [cell]
        return sorted(retval)
