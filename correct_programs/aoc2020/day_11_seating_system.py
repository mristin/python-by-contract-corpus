import re
from typing import Tuple, List, Optional

from icontract import require, ensure


# crosshair: on


@require(lambda i, height: 0 <= i <= height)
@require(lambda j, width: 0 <= j <= width)
@ensure(
    lambda height, width, result: all(
        0 <= i <= height and 0 <= j <= width for i, j in result
    )
)
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


class Layout:
    @require(
        lambda table: len(table) > 0
        and len(table[0]) > 0
        and all(len(row) == len(table[0]) for row in table)
    )
    @require(
        lambda table: all(re.match("^[L#.]\Z", cell) for row in table for cell in row)
    )
    @ensure(lambda self: self.height == len(self.table))
    @ensure(lambda self: len(self.table) > 0 and self.width == len(self.table[0]))
    def __init__(self, table: List[List[str]]) -> None:
        self.table = table
        self.height = len(self.table)
        self.width = len(self.table[0])


@ensure(lambda layout, result: layout.height == result[0].height)
@ensure(lambda layout, result: layout.width == result[0].width)
# fmt: off
@ensure(
    lambda layout, result:
    all(
        (cell == "." and result_cell == ".")
        or (cell != "." and result_cell in ["L", "#"])
        for row, result_row in zip(layout.table, result[0].table)
        for cell, result_cell in zip(row, result_row)
    ),
    "Valid change",
)
# fmt: on
def apply(layout: Layout) -> Tuple[Layout, int]:
    """Return (new layout, number of changes)."""
    new_table = [["" for _ in range(layout.width)] for _ in range(layout.height)]

    change_count = 0

    for i in range(layout.height):
        for j in range(layout.width):
            state = layout.table[i][j]

            if state == ".":
                new_state = "."
            else:
                occupied = 0
                neighbourhood = list_neighbourhood(
                    i=i, j=j, height=layout.height, width=layout.width
                )
                for neighbour_i, neighbour_j in neighbourhood:
                    if layout.table[neighbour_i][neighbour_j] == "#":
                        occupied += 1

                if state == "L" and occupied == 0:
                    new_state = "#"
                    change_count += 1
                elif state == "#" and occupied >= 4:
                    new_state = "L"
                    change_count += 1
                else:
                    new_state = state

            new_table[i][j] = new_state

    return Layout(table=new_table), change_count


def apply_until_stable(layout: Layout) -> Layout:
    change_count = None  # type: Optional[int]
    result = Layout(table=[row[:] for row in layout.table])

    while change_count is None or change_count > 0:
        result, change_count = apply(layout=layout)

    return result


@require(lambda lines: all(re.match(r"^[.L#]+\Z", line) for line in lines))
@require(
    lambda lines: not (len(lines) > 0)
    or all(len(line) == len(lines[0]) for line in lines),
    "Lines are a table",
)
@ensure(lambda lines, result: len(lines) == result.height)
# fmt: off
@ensure(
    lambda lines, result:
    not len(lines) == 0
    or all(len(line) == len(row) for line, row in zip(lines, result))
)
# fmt: on
def parse_layout(lines: List[str]) -> Layout:
    table = []  # type: List[List[str]]
    for line in lines:
        row = []  # type: List[str]
        for symbol in line:
            row.append(symbol)

        table.append(row)

    return Layout(table=table)


def repr_layout(layout: Layout) -> str:
    return "\n".join("".join(row) for row in layout.table)


def count_occupied(layout: Layout) -> int:
    return sum(1 for row in layout.table for cell in row if cell == "#")
