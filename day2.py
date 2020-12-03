from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set

from utils.input_utils import get_input
from utils.log_utils import log


def validate_password_part1(password_line: str) -> bool:
    occurence, letter, password = password_line.split(' ')
    min, max = occurence.split('-')
    letter = letter[0]
    return password.count(letter) >= int(min) and password.count(
        letter) <= int(max)


def validate_password_part2(password_line: str) -> bool:
    positions, letter, password = password_line.split(' ')
    pos1, pos2 = positions.split('-')
    letter = letter[0]
    letter1 = password[int(pos1) - 1]
    letter2 = password[int(pos2) - 1]
    valid = (letter1 == letter
             or letter2 == letter) and not (letter1 == letter2)
    print(f'{valid}  - {password_line}')
    return valid


def count_valid_passwords(passwords: List[str]) -> int:
    cnt = 0
    for password in passwords:
        if validate_password_part2(password):
            cnt += 1

    return cnt


if __name__ == '__main__':
    input_str = get_input('2')
    print(count_valid_passwords(input_str.split('\n')))
