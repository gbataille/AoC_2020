import itertools
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        #         return """16
        # 10
        # 15
        # 5
        # 1
        # 11
        # 7
        # 19
        # 6
        # 12
        # 4"""
        return """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

    return get_input('10')


def run(day_input: str) -> None:
    adapters = list(map(int, day_input.split('\n')))
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    last_jolt = 0
    diffs = {}
    series_length = 0
    comb = 1
    for adapter in adapters:
        d = adapter - last_jolt
        log(f'checking adapter {adapter} with last adapter {last_jolt} and found diff of {d}'
            )

        if d == 1:
            series_length += 1
        else:
            if series_length in [0, 1]:
                pass
            elif series_length == 2:
                comb *= 2
            elif series_length == 3:
                comb *= 4
            elif series_length == 4:
                comb *= 7
            else:
                raise ValueError(f'series_length is invalid {series_length}')

            series_length = 0

        last_jolt = adapter

    print(comb)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
