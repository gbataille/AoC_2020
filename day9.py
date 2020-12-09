import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

    return get_input('9')


def parse_input(day_input: str) -> List[int]:
    return list(map(int, day_input.split('\n')))


def run(day_input: str) -> None:
    preamble = 25
    nums = parse_input(day_input)
    for idx in range(preamble, len(nums)):
        cur_num = nums[idx]
        # if cur_num == 127:
        #     import ipdb
        #     ipdb.set_trace()
        found = False
        for left in nums[idx - preamble:idx]:
            num_idx = {n: True for n in nums[idx - preamble:idx]}
            if (cur_num - left) in num_idx:
                found = True
                break
        if not found:
            invalid_num = cur_num
            break

    print(invalid_num)

    for start in range(len(nums)):
        cumul = nums[start]
        for idx in range(start + 1, len(nums)):
            cumul += nums[idx]
            if cumul == invalid_num:
                res = nums[start:idx + 1]
                log(str(res))
                print(
                    f'min {min(res)}, max: {max(res)}, sum: {min(res) + max(res)}'
                )
            elif cumul > invalid_num:
                break


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
