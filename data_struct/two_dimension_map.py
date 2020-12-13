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

    def __hash__(self):
        return hash(self.to_string())

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    def value_at(self, pos: Position2D) -> T:
        return self.grid[pos.y][pos.x]

    def set_value_at(self, pos: Position2D, value: T) -> None:
        self.grid[pos.y][pos.x] = value

    @staticmethod
    def clone(grid: 'MapGrid[T]', mapper: Callable[[T, Position2D],
                                                   T]) -> 'MapGrid[T]':
        new_map = MapGrid(grid.grid, copy=True)
        for y, row in enumerate(new_map.grid):
            for x, value in enumerate(row):
                new_map.set_value_at(Position2D(x, y),
                                     mapper(value, Position2D(x, y)))
        return new_map

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

    def to_string(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
    ) -> str:
        return line_separator.join(
            list(map(
                value_separator.join,  # type: ignore
                self.grid)))

    def pretty_print(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
    ) -> None:
        print(self.to_string(value_separator, line_separator))

    def count_elem(self, elem_filter: Callable[[T], bool]) -> int:
        cnt = 0
        for row in self.grid:
            for elem in row:
                if elem_filter(elem):
                    cnt += 1

        return cnt
