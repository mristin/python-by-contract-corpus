import re
import sys
from typing import List, Set, Tuple

from icontract import require, ensure

from python_by_contract_corpus.common import Lines


@require(lambda min_time: min_time >= 0)
@require(lambda bus_id: bus_id > 0)
@ensure(lambda result, min_time: result >= min_time)
@ensure(lambda result, min_time, bus_id: result < min_time + bus_id)
@ensure(
    lambda result, min_time: min_time != 0 or result == 0,
    "All buses leave at time zero.",
)
def next_departure(bus_id: int, min_time: int) -> int:
    """Compute the next departure of ``bus_id`` leaving earliest at ``min_time``."""
    # ERROR (pschanely, 2021-04-19):
    # bus_id and min_time should be reversed here.
    wait_time = bus_id % min_time
    return min_time + wait_time


@require(lambda start_time: start_time >= 0)
@require(lambda bus_ids: len(bus_ids) > 0)
@require(lambda bus_ids: all(i > 0 for i in bus_ids))
@ensure(lambda result, start_time: result[0] >= start_time)
@ensure(
    lambda result, bus_ids: result[0] % result[1] == 0,
    "Departure time matches at least one bus.",
)
def find_departure(start_time: int, bus_ids: Set[int]) -> Tuple[int, int]:
    """Find the earliest bus to catch after ``start_time``."""
    return min([(next_departure(bid, start_time), bid) for bid in bus_ids])


# fmt: off
@require(lambda lines: len(lines) == 2)
@require(
    lambda lines:
    len(lines) == 2
    and re.match(r"\d+", lines[0])
    and re.match(r"(\d+|x)(,(\d+|x))*", lines[1])
)
# fmt: on
def parse_input(lines: Lines) -> Tuple[int, Set[int]]:
    """Parse the input into (earliest departure time, bus IDs)."""
    min_time_text, bus_ids_text = lines
    bus_ids = {int(bid) for bid in bus_ids_text.split(",") if bid != "x"}
    return (int(min_time_text), bus_ids)


def main() -> None:
    """Execute the main routine."""
    min_time, bus_ids = parse_input(Lines(sys.stdin.readlines()))
    departure_time, bus_id = find_departure(min_time, bus_ids)
    wait_time = departure_time - min_time
    print(wait_time * bus_id)


if __name__ == "__main__":
    main()
