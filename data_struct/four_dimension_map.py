from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Generic, List, Optional, TypeVar

from data_struct.three_dimension_map import Grid3D, Position3D

T = TypeVar('T')


@dataclass(frozen=True)
class Position4D:
    x: int
    y: int
    z: int
    w: int


class Grid4D(Generic[T]):
    grid: List[Grid3D[T]]

    def __init__(self, grid: List[Grid3D[T]], copy: bool = False):
        self.grid: List[Grid3D[T]] = []
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
    def x_size(self):
        return self.grid[0].x_size

    @property
    def y_size(self):
        return self.grid[0].y_size

    @property
    def z_size(self):
        return self.grid[0].z_size

    @property
    def w_size(self):
        return len(self.grid)

    def value_at(self, pos: Position4D) -> T:
        return self.grid[pos.w].value_at(Position3D(pos.x, pos.y, pos.z))

    def set_value_at(self, pos: Position4D, value: T) -> None:
        self.grid[pos.w].set_value_at(Position3D(pos.x, pos.y, pos.z), value)

    def to_string(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
        slice_separator: str = '------------',
    ) -> str:
        str_value = ''
        for i, w_slice in enumerate(self.grid):
            for j, z_slice in enumerate(w_slice.grid):
                str_value = (
                    f'{str_value}\nw={i}, z={j}:\n{z_slice.to_string(value_separator, line_separator)}\n'
                    f'{slice_separator}\n')

        return str_value

    def clone(self) -> 'Grid4D[T]':
        grid = []
        for w_slice in self.grid:
            grid.append(w_slice.clone())
        return Grid4D(grid)

    def pretty_print(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
        slice_separator: str = '------------',
    ) -> None:
        print(self.to_string(value_separator, line_separator, slice_separator))

    def count_elem(self, elem_filter: Callable[[T], bool]) -> int:
        cnt = 0
        for w_slice in self.grid:
            cnt += w_slice.count_elem(elem_filter)

        return cnt

    def neighbor_values(self, pos: Position4D) -> List[T]:
        neighbors = []
        for x in range(pos.x - 1, pos.x + 2):
            if x < 0 or x >= self.x_size:
                continue

            for y in range(pos.y - 1, pos.y + 2):
                if y < 0 or y >= self.y_size:
                    continue

                for z in range(pos.z - 1, pos.z + 2):
                    if z < 0 or z >= self.z_size:
                        continue

                    for w in range(pos.w - 1, pos.w + 2):
                        if w < 0 or w >= self.w_size:
                            continue

                        if x == pos.x and y == pos.y and z == pos.z and w == pos.w:
                            continue

                        neighbors.append(self.value_at(Position4D(x, y, z, w)))

        return neighbors
