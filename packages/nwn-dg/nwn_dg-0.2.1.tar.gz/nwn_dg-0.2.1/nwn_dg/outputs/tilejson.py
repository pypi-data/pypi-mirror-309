"""
Generate input valid for SetTileJson

https://nwnlexicon.com/index.php/SetTileJson
"""

import json

from .. import constants as C
from ..dungeon import IDungeon


class TileJson(IDungeon):
    def __init__(self, dungeon, data):
        IDungeon.__init__(self, dungeon)

        self._source = data
        self._data = None
        self._output_tile_json = self.args.get("output_tile_json", C.DEFAULT_OUTPUT_TILE_JSON)

    @property
    def data(self):
        return self._data

    def save(self):
        if not self._output_tile_json:
            return

        self.generate()

        filename = self.args["filepath"] + ".tile.json"
        with open(filename, "w", encoding="UTF-8") as fd:
            fd.write(json.dumps(self._data, indent=2))

    def generate(self):
        # Avoid too much indentation
        def tile(x):
            return {"index": x[0], "tileid": x[1]["Tile_ID"]["value"], "orientation": x[1]["Tile_Orientation"]["value"]}

        self._data = {
            "version": "0.2.1",
            "tileset": self._source["Tileset"]["value"],
            "width": self.width,
            "height": self.height,
            "cells": {
                # "rooms": [{"x": cell.x, "y": cell.y} for cell in self.loop_cells() if cell.is_room()],
                # "corridors": [{"x": cell.x, "y": cell.y} for cell in self.loop_cells() if cell.is_corridor()],
                "deadends": [{"x": cell.x, "y": cell.y} for cell in sorted(self.deadends)],
            },
            "rooms": [
                {"identifier": room.identifier, "x": room.center.x, "y": room.center.y} for room in sorted(self.rooms)
            ],
            "tiles": [tile(x) for x in zip(range(self.area), self._source["Tile_List"]["value"])],
        }
