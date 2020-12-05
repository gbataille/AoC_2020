from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


def find_seat(seat_repr: str) -> Tuple[int, int]:
    # Row
    row_repr = seat_repr[:7]
    min_row = 0
    max_row = 127
    for instr in row_repr:
        log(f"""----------------
            min_row: {min_row}
            max_row: {max_row}
            instr:   {instr}""")
        if instr == 'F':
            max_row = int(max_row - (max_row - min_row + 1) / 2)
        else:
            min_row = int(min_row + (max_row - min_row + 1) / 2)

    col_repr = seat_repr[7:]
    min_col = 0
    max_col = 7
    for instr in col_repr:
        if instr == 'L':
            max_col = int(max_col - (max_col - min_col + 1) / 2)
        else:
            min_col = int(min_col + (max_col - min_col + 1) / 2)

    return (min_row, min_col)


def seat_id(seat: Tuple[int, int]) -> int:
    return seat[0] * 8 + seat[1]


if __name__ == '__main__':
    input_str = get_input('5')
    seats = map(find_seat, input_str.split('\n'))
    seat_ids = list(map(seat_id, seats))
    id_idx = {id: True for id in seat_ids}
    min_seat_id = min(seat_ids)
    max_seat_id = max(seat_ids)
    for id in range(min_seat_id, max_seat_id):
        if id in id_idx.keys():
            continue
        else:
            print(id)
            break
