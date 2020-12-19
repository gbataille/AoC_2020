from copy import deepcopy
from typing import List, TypeVar

T = TypeVar('T')


def r_index(search_list: List[T], elem: T) -> int:
    l_copy = deepcopy(search_list)
    l_copy.reverse()
    index = l_copy.index(elem)
    return len(l_copy) - 1 - index
