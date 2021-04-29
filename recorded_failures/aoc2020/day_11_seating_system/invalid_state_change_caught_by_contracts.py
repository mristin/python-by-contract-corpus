import dataclasses
import enum
import re
from typing import Tuple, Mapping, List, Optional, Set, Iterable

from icontract import require, ensure


# crosshair: on

@require(lambda i, height: 0 <= i <= height)
@require(lambda j, width: 0 <= j <= width)
@ensure(lambda height, width, result:
        all(0 <= i <= height and 0 <= j <= width for i, j in result))
@ensure(lambda result: len(result) <= 8)
@ensure(lambda i, j, result: (i, j) not in result)
def list_neighbourhood(
        i: int, j: int, height: int, width: int
) -> List[Tuple[int, int]]:
    # (mristin, 2021-04-03): This would be a nice use case for ensure_each.
    start_i = max(0, i - 1)
    end_i = min(height, i + 2)
    start_j = max(0, j - 1)
    end_j = min(width, j + 2)

    result = []  # type: List[Tuple[int, int]]
    for neighbour_i in range(start_i, end_i):
        for neighbour_j in range(start_j, end_j):
            if neighbour_i == i and neighbour_j == j:
                continue

            result.append((neighbour_i, neighbour_j))

    return result


@require(
    lambda layout:
    not (len(layout) > 0 and len(layout[0]) > 0) or
    all(len(row) == len(layout[0]) for row in layout)
)
@require(lambda layout:
         all(re.match('^[L#.]\Z', cell)
             for row in layout
             for cell in row))
@ensure(lambda result: all(re.match('^[L#.]+\Z', row) for row in result[0]))
@ensure(
    lambda layout, result:
    len(layout) == len(result[0]) and
    all(len(result_row) == len(row) for row, result_row in zip(layout, result[0]))
)
# ERROR: there was an invalid change since the result switched from floor ('.') to '#'.
@ensure(
    lambda layout, result:
    all(
        (cell == '.' and result_cell == '.') or
        (cell != '.' and result_cell in ['L', '#'])
        for row, result_row in zip(layout, result[0])
        for cell, result_cell in zip(row, result_row)
    ),
    "Valid change"
)
def apply(layout: List[List[str]]) -> Tuple[List[List[str]], int]:
    """Return (new layout, number of changes)."""
    height = len(layout)
    width = len(layout[0])

    result = [[''] * width] * height

    change_count = 0

    for i in range(height):
        for j in range(width):
            state = layout[i][j]

            if state == '.':
                new_state = '.'
            else:
                occupied = 0
                neighbourhood = list_neighbourhood(i=i, j=j, height=height, width=width)
                for neighbour_i, neighbour_j in neighbourhood:
                    if layout[neighbour_i][neighbour_j] == '#':
                        occupied += 1

                if state == 'L' and occupied == 0:
                    new_state = '#'
                    change_count += 1
                elif state == '#' and occupied >= 4:
                    new_state = 'L'
                    change_count += 1
                else:
                    new_state = state

            result[i][j] = new_state

    return result, change_count


@require(
    lambda layout:
    not (len(layout) > 0 and len(layout[0]) > 0) or
    all(len(row) == len(layout[0]) for row in layout)
)
@require(lambda layout:
         all(re.match('^[L#.]\Z', cell)
             for row in layout
             for cell in row))
@ensure(lambda result: all(re.match('^[L#.]+\Z', row) for row in result))
@ensure(
    lambda layout, result:
    len(layout) == len(result) and
    all(len(result_row) == len(row) for row, result_row in zip(layout, result))
)
@ensure(
    lambda layout, result:
    all(cell == result_cell
        for row, result_row in zip(layout, result)
        for cell, result_cell in zip(row, result_row)
        if cell == '.'),
    "Floor remains floor"
)
def apply_until_stable(layout: List[List[str]]) -> List[List[str]]:
    change_count = None  # type: Optional[int]
    result = [row[:] for row in layout]

    while change_count is None or change_count > 0:
        result, change_count = apply(layout=layout)

    return result


@require(
    lambda lines: all(re.match(r'^[.L#]+\Z', line) for line in lines)
)
@require(
    lambda lines:
    not (len(lines) > 0) or all(len(line) == len(lines[0]) for line in lines),
    "Lines are a table")
@ensure(lambda lines, result: len(lines) == len(result))
@ensure(
    lambda lines, result:
    not len(lines) == 0 or
    all(len(line) == len(row) for line, row in zip(lines, result))
)
def parse_layout(lines: List[str]) -> List[List[str]]:
    result = []  # type: List[List[str]]
    for line in lines:
        row = []  # type: List[str]
        for symbol in line:
            row.append(symbol)

        result.append(row)

    return result


def repr_layout(layout: List[List[str]]) -> str:
    return '\n'.join(''.join(row) for row in layout)
