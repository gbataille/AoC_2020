import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from data_struct.two_dimension_map import MapGrid, Position2D
from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    return get_input('11')


def run(day_input: str) -> None:
    seat_map = parse_input(day_input)
    seat_map.pretty_print()

    while True:
        # for _ in range(2):
        print('\n\n')
        previous_seat_map = seat_map
        seat_map = apply_round2(seat_map)
        seat_map.pretty_print()

        if seat_map == previous_seat_map:
            break

    print(seat_map.count_elem(lambda elem: elem == '#'))


def parse_input(day_input: str) -> MapGrid[str]:
    return MapGrid.from_string(
        day_input,
        lambda x: x,
    )


def apply_round2(seat_map: MapGrid[str]) -> MapGrid[str]:
    new_seat_map = MapGrid.clone(seat_map, lambda v, pos: v)
    for y, row in enumerate(seat_map.grid):
        for x, seat in enumerate(row):
            neighbors = 0

            log(f"""
checking seat {x},{y}""")
            # top
            for ny in range(y - 1, -1, -1):
                if seat_map.value_at(Position2D(x, ny)) == '#':
                    log("top neighbor found")
                    neighbors += 1
                    break
                if seat_map.value_at(Position2D(x, ny)) == 'L':
                    break
            # top right
            for ny in range(y - 1, -1, -1):
                nx = x + y - ny
                if nx >= seat_map.width:
                    break
                if seat_map.value_at(Position2D(nx, ny)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, ny)) == '#':
                    log("top right neighbor found")
                    neighbors += 1
                    break
            # right
            for nx in range(x + 1, seat_map.width):
                if seat_map.value_at(Position2D(nx, y)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, y)) == '#':
                    log("right neighbor found")
                    neighbors += 1
                    break
            # bottom right
            for ny in range(y + 1, seat_map.height):
                nx = x + ny - y
                if nx >= seat_map.width:
                    break
                if seat_map.value_at(Position2D(nx, ny)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, ny)) == '#':
                    log("bottom right neighbor found")
                    neighbors += 1
                    break
            # bottom
            for ny in range(y + 1, seat_map.height):
                if seat_map.value_at(Position2D(x, ny)) == 'L':
                    break
                if seat_map.value_at(Position2D(x, ny)) == '#':
                    log("bottom neighbor found")
                    neighbors += 1
                    break
            # bottom left
            for ny in range(y + 1, seat_map.height):
                nx = x - (ny - y)
                if nx < 0:
                    break
                if seat_map.value_at(Position2D(nx, ny)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, ny)) == '#':
                    log("bottom left neighbor found")
                    neighbors += 1
                    break
            # left
            for nx in range(x - 1, -1, -1):
                if seat_map.value_at(Position2D(nx, y)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, y)) == '#':
                    log("left neighbor found")
                    neighbors += 1
                    break
            # top left
            for ny in range(y - 1, -1, -1):
                nx = x - (y - ny)
                if nx < 0:
                    break
                if seat_map.value_at(Position2D(nx, ny)) == 'L':
                    break
                if seat_map.value_at(Position2D(nx, ny)) == '#':
                    log("top left neighbor found")
                    neighbors += 1
                    break

            log(f"found {neighbors} neighors")
            if seat == 'L' and neighbors == 0:
                new_seat_map.set_value_at(Position2D(x, y), '#')
                log("seat becomes occupied")
            elif seat == '#' and neighbors > 4:
                new_seat_map.set_value_at(Position2D(x, y), 'L')
                log("seat becomes free")

    return new_seat_map


def apply_round1(seat_map: MapGrid[str]) -> MapGrid[str]:
    new_seat_map = MapGrid.clone(seat_map, lambda v, pos: v)
    for y, row in enumerate(seat_map.grid):
        for x, seat in enumerate(row):
            # neighbors
            min_x = x - 1
            max_x = x + 1
            min_y = y - 1
            max_y = y + 1
            if min_x < 0:
                min_x = 0
            if min_y < 0:
                min_y = 0
            if max_x == seat_map.width:
                max_x -= 1
            if max_y == seat_map.height:
                max_y -= 1

            neighbors = 0
            for ny in range(min_y, max_y + 1):
                for nx in range(min_x, max_x + 1):
                    if ny == y and nx == x:
                        continue
                    seat_value = seat_map.value_at(Position2D(nx, ny))
                    if seat_value == '#':
                        neighbors += 1

            if y == 1:
                log(f"""x={x}, neighbors={neighbors}""")
            if seat == 'L' and neighbors == 0:
                new_seat_map.set_value_at(Position2D(x, y), '#')
            elif seat == '#' and neighbors > 3:
                new_seat_map.set_value_at(Position2D(x, y), 'L')

    return new_seat_map


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
