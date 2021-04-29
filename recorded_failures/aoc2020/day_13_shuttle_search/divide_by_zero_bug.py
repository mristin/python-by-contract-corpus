from typing import Set

from icontract import require, ensure


@require(lambda min_time: min_time >= 0)
@require(lambda bus_id: bus_id > 0)
@ensure(lambda result, min_time: result >= min_time)
@ensure(lambda result, min_time, bus_id: result < min_time + bus_id)
@ensure(
    lambda result, min_time: min_time != 0 or result, "All buses leave at time zero."
)
def next_departure(bus_id: int, min_time: int) -> int:
    # ERROR: when min_time is zero we get ZeroDivisionError here:
    wait_time = bus_id % min_time
    return min_time + wait_time


@require(lambda start_time: start_time >= 0)
@require(lambda bus_ids: len(bus_ids) > 0)
@require(lambda bus_ids: all(i > 0 for i in bus_ids))
@ensure(lambda result, start_time: result >= start_time)
@ensure(
    lambda result, bus_ids: any(result & bid == 0 for bid in bus_ids),
    "Departure time matches at least one bus.",
)
def find_departure(start_time: int, bus_ids: Set[int]) -> int:
    return min([next_departure(bid, start_time) for bid in bus_ids])
