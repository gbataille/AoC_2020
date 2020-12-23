import itertools
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class Rule:
    raw_desc: str
    values: Set[str] = field(default_factory=set)

    def evaluate(self, rules: Dict[int, 'Rule']) -> None:
        if len(self.values) != 0:
            return

        parts = self.raw_desc.split(' | ')

        self._evaluate(parts[0], rules)
        if len(parts) == 2:
            self._evaluate(parts[1], rules)

    def _evaluate(self, raw: str, rules: Dict[int, 'Rule']) -> None:
        pattern = re.match(r'"(\w)"', raw)
        if pattern is not None:
            self.values.add(pattern.group(1))
            return

        subs = raw.split(' ')
        sub_rules = list(map(lambda x: rules[int(x)], subs))

        for rule in sub_rules:
            rule.evaluate(rules)

        products = itertools.product(*list(map(lambda x: x.values, sub_rules)))
        values = set(map(''.join, products))
        self.values = self.values | values


def parse_rules(rules_input: str) -> Dict[int, Rule]:
    rules = {}
    raw_rules = rules_input.split('\n')
    for raw_rule in raw_rules:
        index, raw_desc = raw_rule.split(': ')
        rules[int(index)] = Rule(raw_desc)

    return rules


def get_day_input() -> str:
    if os.environ.get('TEST'):
        return """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
abbbab
aaabbb
aaaabbb"""

    return get_input('19')


def run(day_input: str) -> None:
    raw_rules, raw_comms = day_input.split('\n\n')
    rules = parse_rules(raw_rules)
    rules[0].evaluate(rules)
    print(rules[42])
    print(rules[31])
    # print(rules[8])
    # print(rules[11])

    cnt = 0
    for comm in raw_comms.split('\n'):
        if comm in rules[0].values:
            cnt += 1

    print(cnt)


if __name__ == '__main__':
    input_str = get_day_input()
    run(input_str)
