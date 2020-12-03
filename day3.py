from dataclasses import dataclass, field
from enum import Enum
from functools import partial, reduce
from typing import Iterator, List, Set, Tuple

from data_struct.two_dimension_map import MapGrid
from utils.input_utils import get_input
from utils.log_utils import log


def process_input(input_str: str) -> List[List[int]]:
    rows = input_str.split('\n')
    return list(
        map(lambda row: list(map(lambda x: 1 if x == '#' else 0, row)), rows))


def display_map(input_map: List[List[int]]) -> None:
    for line in input_map:
        log(' '.join(map(str, line)))


def count_trees(input_map: List[List[int]], slope: Tuple[int, int]) -> int:
    nb_trees = 0
    height = len(input_map)
    width = len(input_map[0])
    steps = int(height / slope[1])
    current_position = (0, 0)
    for _i in range(steps - 1):
        current_position = (current_position[0] + slope[0],
                            current_position[1] + slope[1])
        log(str(current_position))
        tree = input_map[current_position[1]][current_position[0] % width]
        log(f'found tree {tree} at [{current_position[0] % width}, {current_position[1]}]'
            )
        nb_trees += tree

    return nb_trees


if __name__ == '__main__':
    input_str = get_input('3')

    mg = MapGrid.from_string(input_str, lambda x: x)
    mg.pretty_print()

    input_map = process_input(input_str)
    display_map(input_map)
    print("""

PART 1

""")
    slope = (3, 1)
    print(count_trees(input_map, slope))
    print("""

PART 2

""")

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = list(map(partial(count_trees, input_map), slopes))
    res = 1
    while trees:
        res *= trees.pop()
    print(res)
