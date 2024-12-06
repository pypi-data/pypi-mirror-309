from .dungeon import Dungeon
from .maps import Sparse
from .outputs import MapPNG, TileJson, Tileset
from .seed import Seed


def generate(args):
    dg = Dungeon(args)
    seed = Seed(args)

    # Compose parts
    Sparse(dg, args)
    MapPNG(dg, args)
    tileset = Tileset(dg, args)
    TileJson(dg, args, tileset)

    # Delete seed first to save the seed in case of future error
    del seed
