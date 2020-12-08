import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class ProgramState:
    acc: int
    iptr: int


def fix_program(instructions: List[str]) -> None:
    for idx in range(len(instructions)):
        log(f'Modifying instr {idx}')
        new_instructions = modify_instr(instructions, idx)

        try:
            program_state = ProgramState(0, 0)
            run_program(new_instructions, program_state)
            print(program_state.acc)
            return
        except ValueError:
            continue


def modify_instr(instructions: List[str], idx: int) -> List[str]:
    instr, offset = instructions[idx].split(' ')
    new_instructions = deepcopy(instructions)

    if instr == 'nop':
        new_instructions[idx] = f'jmp {offset}'
    elif instr == 'jmp':
        new_instructions[idx] = f'nop {offset}'

    return new_instructions


def run_program(instructions: List[str], program_state: ProgramState) -> None:
    seen_iptr = set()
    while True:
        if program_state.iptr == len(instructions):
            return

        log(str(program_state.iptr))
        log(str(program_state.acc))
        log(instructions[program_state.iptr])
        log('----')
        if program_state.iptr in seen_iptr:
            raise ValueError('InfiniteLoop')

        seen_iptr.add(program_state.iptr)
        instr = instructions[program_state.iptr]
        execute_instruction(instr, program_state)


def execute_instruction(instr: str, program_state: ProgramState) -> None:
    cmd, offset = instr.split(' ')
    if cmd == 'nop':
        program_state.iptr += 1
        return

    offset_dir = offset[0]
    offset_value = int(offset[1:])
    if offset_dir == '-':
        offset_value = offset_value * -1

    if cmd == 'acc':
        program_state.acc += offset_value
        program_state.iptr += 1
        return

    if cmd == 'jmp':
        program_state.iptr += offset_value
        return


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

    return get_input('8')


def run(day_input: str) -> None:
    program_instr = day_input.split('\n')
    fix_program(program_instr)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
