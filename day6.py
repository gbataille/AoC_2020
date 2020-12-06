import functools
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def process_input(input_str: str) -> List[Set[str]]:
    groups = []
    group_answers: Optional[Set[str]] = None
    for line in input_str.split('\n'):
        if line == '':
            if group_answers is not None:
                groups.append(list(group_answers))
            group_answers = None
        else:
            if group_answers is None:
                group_answers = set(line)
            else:
                group_answers = group_answers & set(line)
    if group_answers is not None:
        groups.append(list(group_answers))
    return groups


if __name__ == '__main__':
    input_str = get_input('6')
    group_answers = process_input(input_str)
    cnt = 0
    for answers in group_answers:
        cnt += len(list(answers))

    print(cnt)
