import copy
import json
import random
import subprocess
import tempfile

from .. import constants as C
from ..dungeon import IDungeon
from .tilesets import tdc01


class Tileset(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

        self._tileset = None
        self._data = None
        self._patterns = None

        self._output_are = self.args.get("output_are", C.DEFAULT_OUTPUT_ARE)
        self._output_are_json = self.args.get("output_are_json", C.DEFAULT_OUTPUT_ARE_JSON)
        self._output_tile_json = self.args.get("output_tile_json", C.DEFAULT_OUTPUT_TILE_JSON)

    @property
    def data(self):
        return self._data

    def save(self):
        self.generate()

        if True not in [self._output_are, self._output_are_json]:
            return

        filepath = self.args["filepath"]
        with tempfile.NamedTemporaryFile(suffix=".are.json") as tmpfile:
            if self._output_are_json:
                filename = filepath + ".are.json"
            else:
                filename = tmpfile.name
            with open(filename, "w", encoding="UTF-8") as fd:
                fd.write(json.dumps(self.data, indent=2))

            try:
                if self._output_are:
                    filename2 = filepath + ".are"
                    subprocess.run(["nwn_gff", "-i", filename, "-o", filename2], check=True)
            except subprocess.CalledProcessError as err:
                raise SystemExit(f'error: failed to run nwn_gff on "{filename}": {err}') from None

    def generate(self):
        self._tileset = tdc01
        self._data = copy.deepcopy(self._tileset.K_TILESET)

        self._patterns = self._prepare_patterns(self._tileset.K_PATTERNS)
        self._generate_headers()
        self._generate_content()

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
            if not chars:
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

    def _generate_headers(self):
        # TODO: ResRef, Tag, OnExit, OnEnter, ...
        # TODO: Take an input file
        self._data["Height"]["value"] = self.height
        self._data["Width"]["value"] = self.width

    def _generate_content(self):
        # ---
        # dungeon map is (0,0) at the top, but it's bottom left to right, to top
        # in the are file list
        #
        for y in range(self.height, 0, -1):
            y -= 1
            for x in range(self.width):
                cell = self.cells[x][y]
                cells = self.get_bordering_cells(cell)

                k1 = cell.key
                k5 = k1 + "".join([cell.key if cell else "W" for cell in cells])
                for key in [k1, k5]:
                    if key not in self._patterns.keys():
                        continue

                    pattern = self._patterns[key]
                    tileids = pattern["Tile_ID"]
                    tileid = random.sample(tileids, 1)[0]
                    if tileid not in self._tileset.K_TILES:
                        raise SystemExit(f"tileid {tileid} does not exist in tileset tiles")

                    tile = copy.deepcopy(self._tileset.K_TILES[tileid])
                    tile["Tile_Orientation"]["value"] = pattern.get("Tile_Orientation", 0)
                    self._data["Tile_List"]["value"] += [tile]
                    break
