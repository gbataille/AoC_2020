import functools
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

    return get_input('14')


def get_mask(instr: str) -> str:
    return re.match(r'mask = (.*)', instr).group(1)


def update_memory_v1(memory: dict, instr: str, mask: str) -> None:
    addr, value = re.match(r'mem\[(\d*)\] = (\d*)', instr).groups()
    value = int(value)
    bvalue = bin(value)
    bstring = ('0' * 36 + bvalue[2:])[-36:]

    mstring = apply_mask(bstring, mask)
    mvalue = int(mstring, 2)

    memory[addr] = mvalue


def static_mask_for_masks(mask: str) -> List[str]:
    idx = mask.find('X')
    if idx == -1:
        return [mask]

    prefix = mask[:idx]
    sub_masks = static_mask_for_masks(mask[idx + 1:])

    masks = []
    for sub_mask in sub_masks:
        masks.append(prefix + '0' + sub_mask)
        masks.append(prefix + '1' + sub_mask)

    return masks


def addresses_from_mask(mask: str) -> List[int]:
    return list(map(lambda x: int(x, 2), static_mask_for_masks(mask)))


def update_memory_v2(memory: dict, instr: str, mask: str) -> None:
    addr, value = re.match(r'mem\[(\d*)\] = (\d*)', instr).groups()
    addr = int(addr)
    value = int(value)
    baddr = bin(addr)
    bstring = ('0' * 36 + baddr[2:])[-36:]

    mstring = apply_mask(bstring, mask)
    print(mstring)
    addrs = addresses_from_mask(mstring)
    for address in addrs:
        memory[address] = value


def apply_mask(bstring: str, mask: str) -> str:
    if len(bstring) != len(mask):
        raise ValueError('bad input')

    out = []
    for i in range(len(mask)):
        v = bstring[i]
        m = mask[i]
        if m == 'X':
            out.append(m)
        elif m == '0':
            out.append(v)
        else:
            out.append('1')

    return ''.join(out)


def run(day_input: str) -> None:
    instructions = day_input.split('\n')

    mask = '0'
    memory = {}
    for instr in instructions:
        # handle masks
        if instr.startswith('mask'):
            mask = get_mask(instr)
        else:
            # update_memory_v1(memory, instr, mask)
            update_memory_v2(memory, instr, mask)

    print(functools.reduce(lambda x, y: x + y, list(memory.values()), 0))


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
