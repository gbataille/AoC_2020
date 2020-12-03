from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Generic, List, Optional, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class Position2D:
    x: int
    y: int


class MapGrid(Generic[T]):
    grid: List[List[T]]

    def __init__(self, grid: List[List[T]], copy: bool = False):
        self.grid: List[List[T]] = [[]]
        if not grid:
            return

        if copy:
            self.grid = deepcopy(grid)
        else:
            self.grid = grid

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    def value_at(self, pos: Position2D) -> T:
        return self.grid[pos.y][pos.x]

    @staticmethod
    def from_matrix(matrix: List[List[T]]) -> "MapGrid[T]":
        return MapGrid(matrix)

    @staticmethod
    def from_string_list(
        str_list: List[str],
        mapper: Callable[[str], T],
        value_separator: Optional[str] = None,
    ) -> "MapGrid[T]":
        matrix: List[List[T]] = []

        for line in str_list:
            elems: List[str] = []
            if value_separator:
                elems = line.split(value_separator)
            else:
                elems = list(line)

            matrix.append(list(map(mapper, elems)))

        return MapGrid(matrix)

    @staticmethod
    def from_string(
        string: str,
        mapper: Callable[[str], T],
        line_separator: str = '\n',
        value_separator: Optional[str] = None,
    ) -> "MapGrid[T]":
        lines = string.split(line_separator)
        return MapGrid.from_string_list(lines, mapper, value_separator)

    def pretty_print(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
    ) -> None:
        for line in self.grid:
            start_of_line = True
            for value in line:
                if not start_of_line:
                    print(value_separator, end='')

                print(value, end='')

                if start_of_line:
                    start_of_line = False

            print(line_separator, end='')
