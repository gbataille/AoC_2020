import functools
import math
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """939
7,13,x,x,59,x,31,19"""

    return get_input('13')


def parse_input(day_input: str) -> Tuple[int, dict]:
    _time_str, bus_list = day_input.split('\n')

    def fn(acc, elem):
        try:
            i = int(elem[1])
            acc[i] = elem[0]
        except ValueError:
            pass

        return acc

    acc = {}
    functools.reduce(fn, enumerate(bus_list.split(',')), acc)
    return int(bus_list.split(',')[0]), acc


def find_offset(first: int, second: int, offset: int) -> int:
    min_num = min([first, second])
    max_num = max([first, second])

    mult = math.ceil(max_num / min_num)
    delta = (mult * min_num) - max_num

    if offset == first:
        return 0

    first_offset = 0
    if min_num == second:
        offset = offset % second
    if min_num == first:
        first_offset = math.floor(offset / min_num)
        offset = min_num - (offset % min_num)

    i = 1
    cur_delta = delta
    while True:
        if cur_delta == offset:
            if min_num == first:
                return math.ceil(max_num * i / min_num) - 1 - first_offset
            else:
                return i

        i += 1
        cur_delta = (cur_delta + delta) % min_num


def run(day_input: str) -> None:
    first_bus, buses = parse_input(day_input)
    log(buses)
    equations = []
    for bus, index in buses.items():
        if index == 0:
            equations.append((bus, 0))
        else:
            equations.append((bus * first_bus,
                              first_bus * find_offset(first_bus, bus, index)))
            log(f'equation found for {bus}')

    log(equations)

    t = 100000000000000
    t = 100004307610485
    t = 100035967589777
    while True:
        t += equations[0][0]
        log(f'Trying {t}')
        found = True
        for equation in equations[1:]:
            if (t - equation[1]) % equation[0] != 0:
                found = False
                break

        if found:
            print(t)
            return


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
