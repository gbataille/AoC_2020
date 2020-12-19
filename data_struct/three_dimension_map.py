from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Generic, List, Optional, TypeVar

from data_struct.two_dimension_map import MapGrid, Position2D

T = TypeVar('T')


@dataclass(frozen=True)
class Position3D:
    x: int
    y: int
    z: int


class Grid3D(Generic[T]):
    grid: List[MapGrid[T]]

    def __init__(self, grid: List[MapGrid[T]], copy: bool = False):
        self.grid: List[MapGrid[T]] = []
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
        return self.grid[0].width

    @property
    def y_size(self):
        return self.grid[0].height

    @property
    def z_size(self):
        return len(self.grid)

    def value_at(self, pos: Position3D) -> T:
        return self.grid[pos.z].value_at(Position2D(pos.x, pos.y))

    def set_value_at(self, pos: Position3D, value: T) -> None:
        self.grid[pos.z].set_value_at(Position2D(pos.x, pos.y), value)

    def to_string(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
        slice_separator: str = '------------',
    ) -> str:
        str_value = ''
        for i, z_slice in enumerate(self.grid):
            str_value = (
                f'{str_value}\nz={i}:\n{z_slice.to_string(value_separator, line_separator)}\n'
                f'{slice_separator}\n')

        return str_value

    def clone(self) -> 'Grid3D[T]':
        grid = []
        for z_slice in self.grid:
            grid.append(MapGrid.clone(z_slice, lambda x, y: x))
        return Grid3D(grid)

    def pretty_print(
        self,
        value_separator: str = ' ',
        line_separator: str = '\n',
        slice_separator: str = '------------',
    ) -> None:
        print(self.to_string(value_separator, line_separator, slice_separator))

    def count_elem(self, elem_filter: Callable[[T], bool]) -> int:
        cnt = 0
        for z_slice in self.grid:
            cnt += z_slice.count_elem(elem_filter)

        return cnt

    def neighbor_values(self, pos: Position3D) -> List[T]:
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

                    if x == pos.x and y == pos.y and z == pos.z:
                        continue

                    neighbors.append(self.value_at(Position3D(x, y, z)))

        return neighbors
