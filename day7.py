import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterator, List, Optional, Set, Tuple

from utils.input_utils import get_input
from utils.log_utils import log


@dataclass
class BagRule:
    color: str
    children: List[Tuple[int, str]]


@dataclass
class ParentIndex:
    color: str
    parents: List[str]


CONTENT_REGEX = re.compile(r'^ (\d+) ((\w+ ){2})bags?.?$')


def parse_rules(
        rules: str) -> Tuple[Dict[str, BagRule], Dict[str, ParentIndex]]:
    parent_indices: Dict[str, ParentIndex] = {}
    indexed_bag_rules: Dict[str, BagRule] = {}
    for line in rules.split('\n'):
        container, content = line.split('contain')
        parent_color = container[:-6].strip()

        if content == ' no other bags.':
            indexed_bag_rules[parent_color] = BagRule(parent_color, [])
            continue

        children = content.split(',')
        bag_rule = BagRule(parent_color, [])
        for child in children:
            m = CONTENT_REGEX.match(child)
            if m is None:
                raise ValueError(f'regex did not match {child}')
            count = int(m.group(1))
            color = m.group(2).strip()
            bag_rule.children.append((count, color))

            parent_index = parent_indices.get(color)
            if parent_index is None:
                parent_index = ParentIndex(color, [])
                parent_indices[color] = parent_index
            parent_index.parents.append(parent_color)

        indexed_bag_rules[parent_color] = bag_rule

    return (indexed_bag_rules, parent_indices)


def can_contain(content: str, parent_indices: Dict[str,
                                                   ParentIndex]) -> Set[str]:
    parents = set()
    if content not in parent_indices:
        return parents

    for parent in parent_indices[content].parents:
        parents.add(parent)
        parents = parents | can_contain(parent, parent_indices)

    return parents


def nb_children(color: str, bag_rules: Dict[str, BagRule]) -> int:
    cnt = 0
    rules = bag_rules[color]
    for child in rules.children:
        nb_child = child[0]
        color_child = child[1]
        cnt += nb_child
        cnt += nb_child * nb_children(color_child, bag_rules)

    return cnt


if __name__ == '__main__':
    input_str = get_input('7')
    # input_str = """light red bags contain 1 bright white bag, 2 muted yellow bags.
    # dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    # bright white bags contain 1 shiny gold bag.
    # muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    # dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    # faded blue bags contain no other bags.
    # dotted black bags contain no other bags."""
    bag_rules, parent_indices = parse_rules(input_str)
    # for color, children in bag_rules.items():
    #     print(color, children)
    #
    # print('..............')
    # for color, index in parent_indices.items():
    #     print(color, index.parents)
    #
    # print('..............')
    parents = can_contain('shiny gold', parent_indices)
    # log(parents)

    print('part 1')
    print(len(list(parents)))

    print('part 2')
    children = nb_children('shiny gold', bag_rules)
    print(children)
