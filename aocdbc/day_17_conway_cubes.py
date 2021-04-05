import collections
import re
from typing import Tuple, List, Optional, Set, MutableMapping

from icontract import require, ensure

# crosshair: on

Point = Tuple[int, int, int]
Activity = Set[Point]


def are_neighbours(point: Point, another: Point) -> bool:
    return (
        abs(point[0] - another[0]) <= 1
        and abs(point[1] - another[1]) <= 1
        and abs(point[2] - another[2]) <= 1
    )


@ensure(lambda result: len(result) == 26)
@ensure(lambda point, result: point not in result)
# fmt: off
@ensure(
    lambda point, result:
    all(
        are_neighbours(point=point, another=neighbour)
        for neighbour in result
    )
)
# fmt: on
def list_neighbourhood(point: Point) -> List[Point]:
    result = []  # type: List[Point]
    for x in [point[0] - 1, point[0], point[0] + 1]:
        for y in [point[1] - 1, point[1], point[1] + 1]:
            for z in [point[2] - 1, point[2], point[2] + 1]:
                neighbour = (x, y, z)
                if neighbour != point:
                    result.append(neighbour)

    return result


def apply(activity: Activity) -> Activity:
    # Count the number of active neighbours
    votes = collections.defaultdict(lambda: 0)  # type: MutableMapping[Point, int]

    for point in activity:
        for neighbour in list_neighbourhood(point=point):
            votes[neighbour] += 1

    next_activity = set()  # type: Set[Point]
    for point, active_neighbours in votes.items():
        is_active = point in activity

        if is_active:
            if active_neighbours == 2 or active_neighbours == 3:
                next_activity.add(point)
            else:
                pass
        else:
            if active_neighbours == 3:
                next_activity.add(point)

    return next_activity


# fmt: off
@require(
    lambda lines:
    len(lines) >= 1
    and all(
        len(line) == len(lines[0])
        for line in lines
    )
)
# fmt: on
@require(lambda lines: all(re.match(r'^[.#]+\Z', line) for line in lines))
@ensure(lambda lines, result: sum(line.count('#') for line in lines) == len(result))
def parse_initial(lines: List[str]) -> Activity:
    result = set()  # type: Activity

    z = 0
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == '#':
                result.add((x, y, z))

    return result


def repr_activity(activity: Activity) -> str:
    z_set = {point[2] for point in activity}

    xmin = min(point[0] for point in activity)
    xmax = max(point[0] for point in activity)
    ymin = min(point[1] for point in activity)
    ymax = max(point[1] for point in activity)

    z_blocks = []  # type: List[str]

    for z in sorted(z_set):
        block = [f'z={z}']
        for y in range(ymin, ymax + 1):
            line = []  # type: List[str]
            for x in range(xmin, xmax + 1):
                point = (x, y, z)
                if point in activity:
                    line.append('#')
                else:
                    line.append('.')

            block.append(''.join(line))

        z_blocks.append('\n'.join(block))

    return '\n\n'.join(z_blocks)


@ensure(lambda result: result >= 0)
def count_active(activity: Activity) -> int:
    return len(activity)
