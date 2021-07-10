import re
from typing import List, Tuple, Final

from icontract import require, ensure, DBC

# crosshair: on
from python_by_contract_corpus.common import Lines


class RuleParsing:
    """Represent a rule which is not constrained by pre-conditions."""

    identifier: Final[str]  #: Identifier of the field
    ranges: Final[List[Tuple[int, int]]]  #: Valid range of values for the field

    def __init__(self, identifier: str, ranges: List[Tuple[int, int]]) -> None:
        """Initialize with the given values."""
        self.identifier = identifier
        self.ranges = ranges


class Rule(DBC):
    """Represent a rule for the ticket field."""

    identifier: Final[str]  #: identifier of the field
    ranges: Final[List[Tuple[int, int]]]  #: acceptable ranges for the field

    @require(lambda identifier: len(identifier) > 0)
    @require(lambda ranges: all(range[0] < range[1] for range in ranges))
    def __init__(self, identifier: str, ranges: List[Tuple[int, int]]) -> None:
        """Initialize with the given values."""
        self.identifier = identifier
        self.ranges = ranges


def applies(rule: Rule, value: int) -> bool:
    """Check whether the ``rule`` applies to the ``value``."""
    return any(range[0] <= value <= range[1] for range in rule.ranges)


RULE_RE = re.compile(
    r"^([^:]+): "
    r"(0|[1-9][0-9]*)-(0|[1-9][0-9]*)"
    r"( or (0|[1-9][0-9]*)-(0|[1-9][0-9]*))+\Z"
)


@require(lambda lines: all(RULE_RE.match(line) for line in lines))
def parse_rules(lines: Lines) -> List[RuleParsing]:
    """
    Parse the ``lines`` into rules.

     While the parsed rules are syntactically correct, they have to be yet semantically
     verified.
    """
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
    """Parse the nearby tickets from ``lines`` to list of field values."""
    # fmt: off
    return [
        [int(part) for part in line.split(',')]
        for line in lines
    ]
    # fmt: on


# fmt: off
@ensure(
    lambda ticket, result:
    all(
        value in ticket
        for value in result
    )
)
# fmt: on
def invalid_fields(rules: List[Rule], ticket: List[int]) -> List[int]:
    """Select the invalid fields from a ``ticket`` according to ``rules``."""
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
    """Select the invalid fields accross all ``tickets`` according to ``rules``."""
    result = []  # type: List[int]

    for ticket in tickets:
        for value in ticket:
            if not any(applies(rule=rule, value=value) for rule in rules):
                result.append(value)

    return result


def compute_error_rate(invalid_values: List[int]) -> int:
    """Compute the error rate as sum of the invalid values."""
    return sum(invalid_values)
