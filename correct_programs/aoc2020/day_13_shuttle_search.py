import re
import sys
from typing import List, Set, Tuple

from icontract import require, ensure


@require(lambda min_time: min_time >= 0)
@require(lambda bus_id: bus_id > 0)
@ensure(lambda result, min_time: result >= min_time)
@ensure(lambda result, min_time, bus_id: result < min_time + bus_id)
@ensure(
    lambda result, min_time: min_time != 0 or result == 0,
    "All buses leave at time zero.",
)
def next_departure(bus_id: int, min_time: int) -> int:
    missed_last_bus_by = min_time % bus_id
    if missed_last_bus_by == 0:
        return min_time
    else:
        return min_time - missed_last_bus_by + bus_id


@require(lambda start_time: start_time >= 0)
@require(lambda bus_ids: len(bus_ids) > 0)
@require(lambda bus_ids: all(i > 0 for i in bus_ids))
@ensure(lambda result, start_time: result[0] >= start_time)
@ensure(
    lambda result, bus_ids: result[0] % result[1] == 0,
    "Departure time matches at least one bus.",
)
def find_departure(start_time: int, bus_ids: Set[int]) -> Tuple[int, int]:
    return min([(next_departure(bid, start_time), bid) for bid in bus_ids])


@require(lambda lines: len(lines) == 2)
@require(
    lambda lines: (
        len(lines) == 2
        and re.match(r"\d+", lines[0])
        and re.match(r"(\d+|x)(,(\d+|x))*", lines[1])
    )
)
def parse_input(lines: List[str]) -> Tuple[int, Set[int]]:
    min_time_text, bus_ids_text = lines
    bus_ids = {int(bid) for bid in bus_ids_text.split(",") if bid != "x"}
    return (int(min_time_text), bus_ids)


def main() -> None:
    """Execute the main routine."""
    min_time, bus_ids = parse_input(sys.stdin.readlines())
    departure_time, bus_id = find_departure(min_time, bus_ids)
    wait_time = departure_time - min_time
    print(wait_time * bus_id)


if __name__ == "__main__":
    main()
