import functools
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class Rule:
    field_name: str
    ranges: List[Tuple[int]]


@dataclass
class Ticket:
    fields: List[int]

    def __hash__(self):
        return hash(''.join(map(str, self.fields)))

    def __eq__(self, other):
        return hash(self) == hash(other)


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

    return get_input('16')


def parse_input(day_input: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:
    rules_str, my_ticket_str, other_tickets_str = day_input.split('\n\n')
    rules = parse_rules(rules_str)
    my_ticket = parse_my_ticket(my_ticket_str)
    other_tickets = parse_other_tickets(other_tickets_str)
    return (rules, my_ticket, other_tickets)


def parse_rules(rules_input: str) -> List[Rule]:
    rules_str = rules_input.split('\n')
    rules: List[Rule] = []
    for rule_str in rules_str:
        name, ranges_str = rule_str.split(': ')
        range1_str, range2_str = ranges_str.split(' or ')
        ranges: List[Tuple[int]] = []
        ranges.append(tuple(map(int, range1_str.split('-'))))
        ranges.append(tuple(map(int, range2_str.split('-'))))
        rules.append(Rule(name, ranges))

    return rules


def parse_my_ticket(my_ticket_str: str) -> Ticket:
    _title, ticket_str = my_ticket_str.split('\n')
    return Ticket(list(map(int, ticket_str.split(','))))


def parse_other_tickets(other_tickets_str: str) -> List[Ticket]:
    tickets_str = other_tickets_str.split('\n')[1:]
    tickets: List[Ticket] = []
    for ticket_str in tickets_str:
        tickets.append(Ticket(list(map(int, ticket_str.split(',')))))

    return tickets


def invalid_tickets(tickets: List[Ticket], rules: List[Rule]) -> Set[Ticket]:
    invalids = set()
    for ticket in tickets:
        if not is_valid(ticket, rules):
            invalids.add(ticket)

    return invalids


def is_valid(ticket: Ticket, rules: List[Rule]) -> bool:
    for field in ticket.fields:
        valid = False
        for rule in rules:
            if value_matches_rule(field, rule):
                valid = True
                break

        if not valid:
            return False

    return True


def solve_tickets(tickets: List[Ticket], rules: List[Rule]) -> Dict[str, int]:
    clues = {}
    for ticket in tickets:
        try:
            ticket_clues = check_ticket(ticket, rules)
            for ticket_clue in ticket_clues:
                if ticket_clue[0] not in clues.keys():
                    clues[ticket_clue[0]] = ticket_clue[1]
                else:
                    clues[ticket_clue[0]] = clues[
                        ticket_clue[0]] & ticket_clue[1]
        except ValueError:
            pass

    solution = {}
    while len(solution.keys()) != len(rules):
        field_positions = list(clues.keys())
        for field_position in field_positions:
            field_clues = clues[field_position]
            if len(field_clues) == 1:
                field_name = field_clues.pop()
                solution[field_name] = field_position
                del clues[field_position]
                for k in clues.keys():
                    clues[k] = clues[k] - set([field_name])

    return solution


# Returns (field_position, set(possible rules))
def check_ticket(ticket: Ticket,
                 rules: List[Rule]) -> List[Tuple[int, Set[str]]]:
    fields_clues = []
    for i, field in enumerate(ticket.fields):
        matching_rules = set()
        for rule in rules:
            if value_matches_rule(field, rule):
                matching_rules.add(rule.field_name)

        if len(matching_rules) == 0:
            raise ValueError('invalid ticket')
        else:
            fields_clues.append((i, matching_rules))

    return fields_clues


def value_matches_rule(value: int, rule: Rule) -> bool:
    return ((value >= rule.ranges[0][0] and value <= rule.ranges[0][1])
            or (value >= rule.ranges[1][0] and value <= rule.ranges[1][1]))


def run(day_input: str) -> None:
    rules, my_ticket, other_tickets = parse_input(day_input)
    log(rules)
    log(my_ticket)
    log(other_tickets)
    solution = solve_tickets(other_tickets, rules)
    mult = 1
    for field, value in solution.items():
        if field.startswith('departure'):
            mult *= my_ticket.fields[value]

    print(mult)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
