import re
import sys
from collections import defaultdict
from typing import Dict, Set, Tuple

from icontract import require, ensure

from python_by_contract_corpus.common import Lines


@require(lambda text: re.fullmatch(r"\d+ .* bags?", text))
def parse_bagexpr(text: str) -> Tuple[int, str]:
    """
    Parse the expression representing a bag.

    :return: number of units, kind
    """
    match = re.fullmatch(r"(\d+) (.*) bags?", text)
    assert match
    num, kind = match.groups()
    return int(num), kind


@require(lambda text: "\n" not in text)
def parse_rule(text: str) -> Tuple[str, Dict[str, int]]:
    """
    Parse the rule from the text given as a single line.

    :return: kind, contents
    """
    kind, contents_text = text.split(" bags contain ")
    contents: Dict[str, int] = defaultdict(int)
    if contents_text != "no other bags.":
        for subbag_text in contents_text[:-1].split(", "):
            count, subkind = parse_bagexpr(subbag_text)
            contents[subkind] += count
    return kind, contents


Rules = Dict[str, Dict[str, int]]


def parse_rules(lines: Lines) -> Rules:
    """Parse the rules from the given ``lines``."""
    rules: Rules = {}
    for line in lines:
        kind, contents = parse_rule(line)
        rules[kind] = contents
    return rules


def directly_contains(container: str, contained: str, rules: Rules) -> bool:
    """Check whether the ``contained`` is contained in the ``container``."""
    return rules.get(container, {}).get(contained, 0) > 0


# fmt: off
@ensure(
    lambda kind, result: kind in result,
    "given kind is in the result"
)
@ensure(
    lambda kind, rules, result:
    all(
        not directly_contains(non_container, container, rules)
        for non_container in (rules.keys() - result)
        for container in result
    ),
    "Nothing else contains anything in the result",
)
# fmt: on
def containers(kind: str, rules: Rules) -> Set[str]:
    """Compute the set of known containers."""
    known_containers: Set[str] = {kind}
    last_size = 0
    while last_size < len(known_containers):
        last_size = len(known_containers)
        for container_kind, subbags in rules.items():
            for (contents_kind, _ct) in subbags.items():
                if contents_kind in known_containers:
                    known_containers.add(container_kind)
    return known_containers


def count_containers(lines: Lines) -> int:
    """Parse the rules given as ``lines`` and count the allowed containers."""
    rules = parse_rules(lines)
    allowed_containers = containers("shiny gold", rules)
    assert allowed_containers is not None
    return len(allowed_containers) - 1


def main() -> None:
    """Execute the main routine."""
    lines = Lines(sys.stdin.read().splitlines())
    print(count_containers(lines))


if __name__ == "__main__":
    main()
