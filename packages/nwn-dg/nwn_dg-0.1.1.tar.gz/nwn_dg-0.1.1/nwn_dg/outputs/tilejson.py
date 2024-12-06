"""
Generate input valid for SetTileJson

https://nwnlexicon.com/index.php/SetTileJson
"""

import json

from ..proxy import DungeonProxy


class TileJson(DungeonProxy):
    def __init__(self, dungeon, args, tileset):
        DungeonProxy.__init__(self, dungeon)
        self._filepath = args["filepath"]
        self._output_tile_json = args.get("output_tile_json", False)
        self._tiles = tileset.output
        self._output = []

        if not self._output_tile_json:
            return

        self._output = self.generate()

    def generate(self):
        index = 0
        retval = []
        for tile in self._tiles["Tile_List"]["value"]:
            retval += [
                {
                    "index": index,
                    "tileid": tile["Tile_ID"]["value"],
                    "orientation": tile["Tile_Orientation"]["value"],
                },
            ]
            index += 1
        return retval

    def __del__(self):
        if not self._output_tile_json:
            return

        filename = self._filepath + ".tile.json"
        with open(filename, "w", encoding="UTF-8") as fd:
            fd.write(json.dumps(self._output, indent=2))
