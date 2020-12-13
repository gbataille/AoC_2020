import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


class Direction(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


@dataclass
class Position:
    north: int = 0
    east: int = 0


@dataclass
class Ship:
    ship_position: Position
    waypoint_position: Position

    def execute_instr(self, instr: str) -> None:
        command = instr[0]
        qty = int(instr[1:])

        try:
            direction = Direction(command)
            self.move_waypoint(direction, qty)
            return
        except ValueError:
            pass

        if command == 'F':
            self.move_forward(qty)
        if command == 'L':
            self.turn_left(qty)
        if command == 'R':
            self.turn_right(qty)

    def move_north(self, qty: int) -> None:
        self.waypoint_position.north += qty

    def move_east(self, qty: int) -> None:
        self.waypoint_position.east += qty

    def move_south(self, qty: int) -> None:
        self.waypoint_position.north -= qty

    def move_west(self, qty: int) -> None:
        self.waypoint_position.east -= qty

    def move_waypoint(self, direction: Direction, qty: int) -> None:
        if direction == Direction.NORTH:
            self.move_north(qty)
        elif direction == Direction.EAST:
            self.move_east(qty)
        elif direction == Direction.SOUTH:
            self.move_south(qty)
        elif direction == Direction.WEST:
            self.move_west(qty)

    def move_forward(self, qty: int) -> None:
        self.ship_position.north += qty * self.waypoint_position.north
        self.ship_position.east += qty * self.waypoint_position.east

    def turn_right(self, qty: int) -> None:
        steps = abs(int(qty / 90))
        direction = int(qty / abs(qty))
        for _ in range(steps):
            temp = self.waypoint_position.east
            self.waypoint_position.east = self.waypoint_position.north * direction
            self.waypoint_position.north = -1 * temp * direction

    def turn_left(self, qty: int) -> None:
        self.turn_right(-qty)


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """F10
N3
F7
R90
F11"""

    return get_input('12')


def run(day_input: str) -> None:
    instructions = day_input.split('\n')
    ship = Ship(Position(), Position(1, 10))
    for instr in instructions:
        ship.execute_instr(instr)
        log(instr)
        log(str(ship))

    print(abs(ship.ship_position.east) + abs(ship.ship_position.north))


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
