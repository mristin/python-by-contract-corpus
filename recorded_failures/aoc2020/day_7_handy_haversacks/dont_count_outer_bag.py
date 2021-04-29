from collections import defaultdict
import re
import sys
from typing import Dict, Set, Tuple

from icontract import require, ensure


@require(lambda text: re.fullmatch(r"\d+ .* bags?", text))
def parse_bagexpr(text: str) -> Tuple[int, str]:
    match = re.fullmatch(r"(\d+) (.*) bags?", text)
    assert match
    num, kind = match.groups()
    return (int(num), kind)


def parse_rule(text: str) -> Tuple[str, Dict[str, int]]:
    kind, contents_text = text.split(" bags contain ")
    contents: Dict[str, int] = defaultdict(int)
    if contents_text != "no other bags.":
        for subbag_text in contents_text[:-1].split(", "):
            count, subkind = parse_bagexpr(subbag_text)
            contents[subkind] += count
    return (kind, contents)


Rules = Dict[str, Dict[str, int]]


def parse_rules(text: str) -> Rules:
    rules: Rules = {}
    for line in text.splitlines():
        kind, contents = parse_rule(line)
        rules[kind] = contents
    return rules


# @require()
# def direct_containers(kind: str, rules: Rules) -> Iterable[str]:
#     for container_kind, subbags in rules.items():
#         for (contents_kind, _ct) in subbags.items():
#             if contents_kind == kind:
#                 yield container_kind


def directly_contains(container: str, contained: str, rules: Rules) -> bool:
    return rules.get(container, {}).get(contained, 0) > 0


@ensure(lambda kind, result: kind in result)
@ensure(
    lambda kind, rules, result: all(
        not directly_contains(non_container, container, rules)
        for non_container in (rules.keys() - result)
        for container in result
    ),
    "Nothing else contains anything in the result",
)
def containers(kind: str, rules: Rules) -> Set[str]:
    known_containers: Set[str] = {kind}
    last_size = 0
    while last_size < len(known_containers):
        last_size = len(known_containers)
        for container_kind, subbags in rules.items():
            for (contents_kind, _ct) in subbags.items():
                if contents_kind in known_containers:
                    known_containers.add(container_kind)
                    # del rules[container_kind]
    return known_containers


def part1(text: str) -> int:
    rules = parse_rules(text)
    return len(containers("shiny gold", rules)) - 1


def rules_are_valid(rules: Rules):
    # Every kind mentioned is defined
    for subbags in rules.values():
        for subkind in subbags.keys():
            if subkind not in rules:
                return False
    return True


@require(lambda rules: rules_are_valid(rules))
@require(lambda kind, rules: kind in rules)
@ensure(lambda kind, rules, result: (result == 0) == (len(rules[kind]) == 0))
@ensure(lambda kind, rules, result: result >= sum(rules[kind].values()))
def count_bags(kind: str, rules: Rules) -> int:
    # ERROR: return is too high by one - you don't count the outermost bag.
    count = 1
    for subkind, ct in rules[kind].items():
        count += count_bags(subkind, rules) * ct
    return count
