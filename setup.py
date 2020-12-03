import os
import sys

import requests

CURDIR = os.path.dirname(__file__)


def setup_day(day: int):
    day_folder = os.path.join(CURDIR, str(day))
    if not os.path.isdir(day_folder):
        print(f"Creating {day_folder}")
        os.mkdir(day_folder)

    day_input = os.path.join(day_folder, 'input.csv')
    if os.path.isfile(day_input):
        print(f"Input file {day_input} already exists")
    else:
        resp = requests.get(
            f"https://adventofcode.com/2020/day/{day}/input",
            cookies={
                'session':
                "53616c7465645f5fb5a5085340e25f56b23f243eb3ca730b69cee444f4d94d51302304415f3d5f16f402dad5f2951a60"
            })
        with open(day_input, 'wb') as input_file:
            input_file.write(resp.content)

        with open(f'day{str(day)}.py', 'w') as code_file:
            code_file.write(f"""from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


if __name__ == '__main__':
    input_str = get_input('{str(day)}')
    print(input_str)""")


if __name__ == '__main__':
    day = int(sys.argv[1])
    setup_day(day)
