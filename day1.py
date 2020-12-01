from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set

from input_utils import get_input
from log_utils import log

if __name__ == '__main__':
    input_str = get_input('1')
    input_arr = [int(i) for i in input_str.split('\n')]
    input_arr.sort()
    idx = {key: True for key in input_arr}

    for elem in input_arr:
        comp = 2020 - int(elem)

        for elem2 in input_arr:
            if elem == elem2:
                continue
            if elem2 > comp:
                continue

            comp2 = comp - elem2
            if comp2 in idx.keys():
                print(elem, elem2, comp2)
                print(elem * elem2 * comp2)
                break
