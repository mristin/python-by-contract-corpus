import re
from typing import List, Mapping, MutableMapping, Tuple, Final

from icontract import require, ensure, DBC


# crosshair: on
from correct_programs import common


class RuleParsing:
    """Represent a rule which is not constrained by pre-conditions."""

    identifier: Final[str]
    ranges: Final[List[Tuple[int, int]]]

    def __init__(self, identifier: str, ranges: List[Tuple[int, int]]) -> None:
        self.identifier = identifier
        self.ranges = ranges


class Rule(DBC):
    identifier: Final[str]
    ranges: Final[List[Tuple[int, int]]]

    @require(lambda identifier: len(identifier) > 0)
    @require(lambda ranges: all(range[0] < range[1] for range in ranges))
    def __init__(self, identifier: str, ranges: List[Tuple[int, int]]) -> None:
        self.identifier = identifier
        self.ranges = ranges


def applies(rule: Rule, value: int) -> bool:
    return any(range[0] <= value <= range[1] for range in rule.ranges)


RULE_RE = re.compile(
    r"^([^:]+): "
    r"(0|[1-9][0-9]*)-(0|[1-9][0-9]*)"
    r"( or (0|[1-9][0-9]*)-(0|[1-9][0-9]*))+\Z"
)


@require(lambda lines: all(RULE_RE.match(line) for line in lines))
def parse_rules(lines: common.Lines) -> List[RuleParsing]:
    result = []  # type: List[RuleParsing]
    for line in lines:
        identifier, rest = line.split(": ", 1)

        ranges = []  # type: List[Tuple[int, int]]

        for part in rest.split(" or "):
            first, last = part.split("-")

            ranges.append((int(first), int(last)))

        result.append(RuleParsing(identifier=identifier, ranges=ranges))

    return result


# fmt: off
@require(
    lambda lines:
    all(
        re.match(r'^(0|[1-9][0-9]*)(,(0|[1-9][0-9]*))+\Z', line)
        for line in lines
    )
)
# fmt: on
def parse_nearby_tickets(lines: List[str]) -> List[List[int]]:
    # fmt: off
    return [
        [int(part) for part in line.split(',')]
        for line in lines
    ]
    # fmt: on


@ensure(lambda ticket, result: all(value in ticket for value in result))
def invalid_fields(rules: List[Rule], ticket: List[int]) -> List[int]:
    result = []  # type: List[int]
    for value in ticket:
        if not any(applies(rule=rule, value=value) for rule in rules):
            result.append(value)

    return result


# fmt: off
@ensure(
    lambda tickets, result:
    all(
        any(value in ticket for ticket in tickets)
        for value in result
    )
)
# fmt: on
def list_all_invalid_values(rules: List[Rule], tickets: List[List[int]]) -> List[int]:
    result = []  # type: List[int]

    for ticket in tickets:
        for value in ticket:
            if not any(applies(rule=rule, value=value) for rule in rules):
                result.append(value)

    return result


def compute_error_rate(invalid_values: List[int]) -> int:
    return sum(invalid_values)
