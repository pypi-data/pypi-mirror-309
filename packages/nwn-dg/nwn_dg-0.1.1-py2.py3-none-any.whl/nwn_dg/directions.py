from enum import Enum


class Directions(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


DIRECTIONS_X = {Directions.NORTH: 0, Directions.SOUTH: 0, Directions.EAST: 1, Directions.WEST: -1}
DIRECTIONS_Y = {Directions.NORTH: -1, Directions.SOUTH: 1, Directions.EAST: 0, Directions.WEST: 0}
DIRECTIONS = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]


def get_new_position(x, y, direction):
    n_x = x + DIRECTIONS_X[direction]
    n_y = y + DIRECTIONS_Y[direction]
    return n_x, n_y


def get_clockwise(direction):
    return {
        Directions.NORTH: Directions.EAST,
        Directions.EAST: Directions.SOUTH,
        Directions.SOUTH: Directions.WEST,
        Directions.WEST: Directions.NORTH,
    }[direction]


def get_counterclockwise(direction):
    return {
        Directions.NORTH: Directions.WEST,
        Directions.EAST: Directions.NORTH,
        Directions.SOUTH: Directions.EAST,
        Directions.WEST: Directions.SOUTH,
    }[direction]


def get_4_cells(dg, x, y):
    def get_cell(x, y, direction):
        x, y = get_new_position(x, y, direction)
        if x < 0 or y < 0:
            return None
        if x >= dg.width or y >= dg.height:
            return None
        return dg.cells[x][y]

    n_cell = get_cell(x, y, Directions.NORTH)
    e_cell = get_cell(x, y, Directions.EAST)
    s_cell = get_cell(x, y, Directions.SOUTH)
    w_cell = get_cell(x, y, Directions.WEST)
    return n_cell, e_cell, s_cell, w_cell
