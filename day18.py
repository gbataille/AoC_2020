import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional, Set, Tuple, Union

from utils import array_utils
from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class Tree:
    operator: str
    left_operand: Union[int, 'Tree']
    right_operand: Union[int, 'Tree']


def build_tree(tokens: List[str]) -> Tree:
    first_char = tokens.pop()
    if first_char == '(':
        end_sub_expr = find_matching_closing_reverse(tokens)
        left_operand = build_tree(tokens[end_sub_expr + 1:])
        tokens = tokens[:end_sub_expr]
    else:
        left_operand = int(first_char)

    tokens.pop()
    operator = tokens.pop()
    tokens.pop()


def evaluate_tree(tree: Tree) -> int:
    if type(tree.left_operand) == 'int':
        left = tree.left_operand
    else:
        left = evaluate_tree(tree.left_operand)

    if type(tree.right_operand) == 'int':
        right = tree.right_operand
    else:
        right = evaluate_tree(tree.right_operand)

    if tree.operator == '+':
        return left + right
    else:
        return left * right


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """1 + (2 * 3) + (4 * (5 + 6))"""

    return get_input('18')


def apply_operation(first_elem: int, operator: str, second_elem: int) -> int:
    log(f'Appling operation {first_elem} { operator} {second_elem}')
    if operator == '+':
        return first_elem + second_elem
    elif operator == '*':
        return first_elem * second_elem
    else:
        raise ValueError('unknown operator')


def find_matching_closing(tokens: List[str]) -> int:
    log(f'Looking for closing parentheses in {tokens}')
    opened = 1
    for idx, char in enumerate(tokens):
        if char == '(':
            opened += 1
        if char == ')':
            opened -= 1

        if opened == 0:
            return idx

    raise ValueError('closing parentheses not found')


def find_matching_closing_reverse(tokens: List[str]) -> int:
    tokens_copy = list(tokens)
    tokens_copy.reverse()
    idx = find_matching_closing(tokens_copy)
    return len(tokens) - 1 - idx


def evaluate_operation(tokens: List[str]) -> int:
    log(f'evaluating {tokens}')
    first_char = tokens.pop()
    if first_char == '(':
        end_sub_expr = find_matching_closing_reverse(tokens)
        first_elem = evaluate_operation(tokens[end_sub_expr + 1:])
        tokens = tokens[:end_sub_expr]
    else:
        first_elem = int(first_char)

    try:
        while True:
            tokens.pop()
            operator = tokens.pop()
            tokens.pop()
            next_char = tokens.pop()
            if next_char == '(':
                end_sub_expr = find_matching_closing_reverse(tokens)
                second_elem = evaluate_operation(tokens[end_sub_expr + 1:])
                tokens = tokens[:end_sub_expr]
            else:
                second_elem = int(next_char)

            first_elem = apply_operation(first_elem, operator, second_elem)

    except IndexError:
        return first_elem


def run(day_input: str) -> None:
    operations = day_input.split('\n')
    tot = 0
    for operation in operations:
        expr = list(operation)
        expr.reverse()
        tot += evaluate_operation(expr)

    print(tot)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
