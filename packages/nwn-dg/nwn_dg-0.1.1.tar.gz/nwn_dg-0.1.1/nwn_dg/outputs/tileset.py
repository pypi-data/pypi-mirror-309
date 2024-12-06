import copy
import json
import os
import random
import subprocess

from ..directions import get_4_cells
from ..proxy import DungeonProxy
from .tilesets import tdc01


class Tileset(DungeonProxy):
    def __init__(self, dungeon, args):
        DungeonProxy.__init__(self, dungeon)
        self._filepath = args["filepath"]

        self._output_are_json = args.get("output_are_json", True)
        self._output_are = args.get("output_are", False)

        # If we don't need to calculate anything, then don't
        if not any([self._output_are_json, self._output_are, args.get("output_json")]):
            return

        # We need to generate tileset json only if SetTileJson data is required
        # or "are" file is required
        self._ts = tdc01
        self._output = copy.deepcopy(self._ts.K_BASEDATA)
        self._patterns = self._prepare_patterns(self._ts.K_PATTERNS)
        self._tiles = self._ts.K_TILES

        self.change_headers()
        self.generate()

    @property
    def output(self):
        return self._output

    def __del__(self):
        if not any([self._output_are_json, self._output_are]):
            return

        filename = self._filepath + ".are.json"
        with open(filename, "w", encoding="UTF-8") as fd:
            fd.write(json.dumps(self._output, indent=2))

        try:
            if self._output_are:
                filename2 = self._filepath + ".are"
                subprocess.run(["nwn_gff", "-i", filename, "-o", filename2], check=True)
        except subprocess.CalledProcessError as err:
            raise SystemExit(f'error: failed to run nwn_gff on "{filename}": {err}') from None
        finally:
            if not self._output_are_json:
                os.remove(self._output_are_json)

    def _prepare_patterns(self, patterns):
        def get_orientations(c0, pattern):
            # Rotate with C.1234 becomes C.4123
            retval = []
            for i in range(1, 4):
                pattern = pattern[1:] + pattern[0]
                retval += [(i, c0 + pattern)]
            return retval

        # Do all permutations
        retval = copy.deepcopy(patterns)
        for pattern, tiles in patterns.items():
            c0 = pattern[0]
            chars = pattern[1:]
            if len(chars) == 0:
                continue

            orientations = get_orientations(c0, chars)
            for orientation, key in orientations:
                # if it already exists, skip it
                if key in retval.keys():
                    continue
                tiles = copy.deepcopy(tiles)
                tiles["Tile_Orientation"] = orientation
                retval[key] = tiles
        return retval

    def change_headers(self):
        if not any([self._output_are_json, self._output_are]):
            return

        # TODO: ResRef, Tag, OnExit, OnEnter, ...
        # TODO: Take an input file
        self._output["Height"]["value"] = self.height
        self._output["Width"]["value"] = self.width

    def generate(self):
        def get_key(cells):
            retval = ""
            for cell in cells:
                if cell is None:
                    retval += "W"
                elif cell.is_corridor():
                    retval += "C"
                elif cell.is_room():
                    retval += "R"
                else:
                    retval += "W"
            return retval

        def set_tile(keys):
            for key in keys:
                if key not in self._patterns.keys():
                    continue

                cell_pattern = self._patterns[key]
                tileids = cell_pattern["Tile_ID"]
                random.shuffle(tileids)
                tileid = tileids[0]

                if tileid not in self._tiles:
                    raise SystemExit(f"tileid {tileid} does not exist in tileset tiles")

                tile = copy.deepcopy(self._tiles[tileid])
                tile["Tile_Orientation"]["value"] = cell_pattern.get("Tile_Orientation", 0)
                self._output["Tile_List"]["value"] += [tile]
                return True
            return False

        # dungeon map is (0,0) at the top, but it's bottom left to right, to top
        # in the are file list
        for y in range(self.height, 0, -1):
            y -= 1
            for x in range(self.width):
                cell = self.cells[x][y]
                cells = get_4_cells(self._dg, x, y)

                k1 = get_key([cell])
                k5 = k1 + get_key(cells)

                # TODO: temporary fix
                if not set_tile([k1, k5, "W"]):
                    set_tile(["W"])
                    raise SystemExit(f"key not found: {k1},{k5} for {cell}")
