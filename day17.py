import functools
import itertools
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from data_struct.four_dimension_map import Grid4D, Position4D
from data_struct.three_dimension_map import Grid3D, Position3D
from data_struct.two_dimension_map import MapGrid, Position2D
from utils.input_utils import get_input
from utils.log_utils import log

NB_ITERATION = 6


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """.#.
..#
###"""

    return get_input('17')


def parse_input(day_input: str) -> Grid4D[str]:
    rows = list(map(lambda x: list(x), day_input.split('\n')))
    input_height = len(rows)
    input_width = len(rows[0])

    space_height = NB_ITERATION + input_height + NB_ITERATION
    space_width = NB_ITERATION + input_width + NB_ITERATION

    z_slices = []
    empty_slice = ['.' * space_width] * space_height
    for _ in range(NB_ITERATION):
        z_slices.append(MapGrid.from_string_list(empty_slice, lambda x: x))

    input_slice = []
    for _ in range(NB_ITERATION):
        input_slice.append(''.join('.' * space_width))
    for row in rows:
        input_slice.append(
            f"{''.join('.' * NB_ITERATION)}{''.join(row)}{''.join('.' * NB_ITERATION)}"
        )
    for _ in range(NB_ITERATION):
        input_slice.append(''.join('.' * space_width))

    z_slices.append(MapGrid.from_string_list(input_slice, lambda x: x))

    for _ in range(NB_ITERATION):
        z_slices.append(MapGrid.from_string_list(empty_slice, lambda x: x))

    middle_w = Grid3D(z_slices)

    empty_grid3d = Grid3D(
        [MapGrid.from_string_list(empty_slice, lambda x: x)] *
        (NB_ITERATION + 1 + NB_ITERATION))

    return Grid4D(
        list(itertools.repeat(empty_grid3d, NB_ITERATION)) + [middle_w] +
        list(itertools.repeat(empty_grid3d, NB_ITERATION)))


def run(day_input: str) -> None:
    grid = parse_input(day_input)
    # print(grid)
    # print(grid.grid[0])
    # print(grid.grid[0].grid[0])
    # grid.pretty_print()

    for _iteration in range(NB_ITERATION):
        new_grid = grid.clone()
        for x in range(grid.x_size):
            for y in range(grid.y_size):
                for z in range(grid.z_size):
                    for w in range(grid.w_size):
                        cur_pos = Position4D(x, y, z, w)
                        neighbors = grid.neighbor_values(cur_pos)
                        cnt = 0
                        for n in neighbors:
                            if n == '#':
                                cnt += 1

                        if grid.value_at(cur_pos) == '#':
                            if cnt not in [2, 3]:
                                new_grid.set_value_at(cur_pos, '.')
                        else:
                            if cnt == 3:
                                new_grid.set_value_at(cur_pos, '#')

        grid = new_grid

    # grid.pretty_print()
    print(grid.count_elem(lambda x: x == '#'))


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
