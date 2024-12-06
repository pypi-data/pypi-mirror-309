"""
Main command-line interface
"""

import argparse
import sys

from torxtools import argtools

from . import generator
from .constants import DEFAULT_GRID_SIZE


def _options(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="nwn-dg",
        description="Neverwinter Nights (nwn) dungeon generator",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

    # fmt: off
    parser.add_argument('--seed', metavar='SEED', help="Initialization seed for random.seed(). If a file is passed, it's content will be used to restore state.")
    parser.add_argument('--output-seed', action=argparse.BooleanOptionalAction, default=False, help="Output the seed to a file. (default: false)")

    # map
    group = parser.add_argument_group('map')
    group.add_argument('--map-width', metavar='WIDTH', type=int, default=17, action=argtools.is_int_positive, help="Map height (default: 17)")
    group.add_argument('--map-height', metavar='HEIGHT', type=int, default=17, action=argtools.is_int_positive, help="Map width (default: 17)")
    group.add_argument('--map-deadends-pct', metavar='PCT', type=int, default=50, action=argtools.is_int_between(0,100), help="Deadends, as a percentage (0-100) to keep")
    group.add_argument('--map-bend-pct', metavar='PCT', type=int, default=50, action=argtools.is_int_between(0,100), help="Corridors bend this percentage of the time (0-100)")
    group.add_argument('--map-reshape-pct', metavar='PCT', type=int, default=70, action=argtools.is_int_between(0,100), help="Whether to reshape rooms to avoid only square rooms, as a percentage (default: 70)")
    group.add_argument('--map-min-rooms', metavar='NUMBER', type=int, default=1, action=argtools.is_int_positive, help="Minimum number of rooms")
    group.add_argument('--map-max-rooms', metavar='NUMBER', type=int, default=None, action=argtools.is_int_positive, help="Maximum number of rooms")
    group.add_argument('--map-room-ratio', metavar='PCT', type=int, default=100, action=argtools.is_int_between(1,100), help="Percentage of rooms to create according to dimensions of map (default: 100)")

    # png
    group = parser.add_argument_group('png')
    group.add_argument('--output-png', action=argparse.BooleanOptionalAction, default=True, help="Output a png map. (default: true)")
    group.add_argument('--png-grid-size', action=argtools.is_int_positive, metavar='SIZE', type=int, default=DEFAULT_GRID_SIZE, help=f"Grid size, in pixels, of png map (default: {DEFAULT_GRID_SIZE})")
    group.add_argument('--png-room-ids', action=argparse.BooleanOptionalAction, default=True, help="Output room identifier (default: true)")

    # are
    group = parser.add_argument_group('are')
    group.add_argument('--output-are-json', action=argparse.BooleanOptionalAction, default=True, help="Output a nwn 'are' json file. (default: true)")
    group.add_argument('--output-are', action=argparse.BooleanOptionalAction, default=False, help="Output a nwn 'are' file converted with `nwn_gff`. (default: false)")

    # json
    group = parser.add_argument_group('tile json')
    group.add_argument('--output-tile-json', action=argparse.BooleanOptionalAction, default=False, help="Output a json file suitable for SetTileJson(). (default: false)")

    # Outputs: tileset are, tile json, png, graph png
    parser.add_argument('filepath', help="Output base filepath. Extensions will be added according to output file type")
    # fmt: on

    try:
        return vars(parser.parse_args(argv))
    except argparse.ArgumentTypeError as err:
        raise SystemExit(f"error: {err}") from None


def main():
    args = _options()
    generator.generate(args)
