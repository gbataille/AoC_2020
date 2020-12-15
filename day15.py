import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """0,3,6"""

    return get_input('15')


def run(day_input: str) -> None:
    serie = list(map(int, day_input.split(',')))
    memory = {num: (-1, pos) for pos, num in enumerate(serie)}
    index = len(serie)
    last_number = serie[-1]
    log(f'starting with index {index}, memory {memory}')
    while True:
        appearances = memory.get(last_number, None)
        if appearances[0] == -1:
            last_number = 0
        else:
            last_number = appearances[1] - appearances[0]

        serie.append(last_number)
        memory[last_number] = (memory.get(last_number, (-1, -1))[1], index)

        index += 1

        if index == 30000000:
            break

    print(last_number)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
