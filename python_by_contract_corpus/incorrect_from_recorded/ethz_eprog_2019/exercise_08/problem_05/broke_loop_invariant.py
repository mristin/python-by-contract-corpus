"""
Simulate the wolf fleeing a city.

A city is given as a grid of ``n x n`` crossroads. At each crossroad, the wolf picks
a random direction. The grid size ``n`` is greater than 1 and odd.

The wolf starts at ``(0, 0)``. The wolf escaped the city when he reaches the border
of the grid.

The wolf can never visit the same crossroad twice. If there are no more options,
the wolf is shot by the hunters and dies.

Estimate the probability of the wolf escaping the city.

(We deliberately exclude the parts of the exercise concerning the drawing of the paths
in the GUI.)
"""
import random
from typing import Set, Sequence, Optional, Final

from icontract import require, ensure


class Position:
    """Represent the current position of the wolf on the grid."""

    x: Final[int]  #: X-coordinate of the cell
    y: Final[int]  #: Y-coordinate of the cell

    def __init__(self, x: int, y: int) -> None:
        """Initialize with the given values."""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r})"


# fmt: off
@ensure(lambda result: len(result) == 4)
@ensure(lambda pos, result: pos not in result)
@ensure(
    lambda pos, result:
    all(
        not (next_pos.x != pos.x) or (abs(next_pos.x - pos.x) == 1)
        for next_pos in result
    ),
    "Next is at most 1 field in x-direction"
)
@ensure(
    lambda pos, result:
    all(
        not (next_pos.y != pos.y) or (abs(next_pos.y - pos.y) == 1)
        for next_pos in result
    ),
    "Next is at most 1 field in y-direction"
)
@ensure(
    lambda pos, result:
    all(
        (next_pos.x == pos.x and next_pos.y != pos.y)
        ^ (next_pos.x != pos.x and next_pos.y == pos.y)
        for next_pos in result
    ),
    "Next is either in x- or in y-direction"
)
# fmt: on
def list_next_positions(pos: Position) -> Sequence[Position]:
    """List all the possible next positions based on the current position ``pos``."""
    return (
        Position(x=pos.x + 1, y=pos.y),
        Position(x=pos.x, y=pos.y + 1),
        Position(x=pos.x - 1, y=pos.y),
        Position(x=pos.x, y=pos.y - 1),
    )


@require(lambda trials: trials > 0)
@require(lambda grid_size: grid_size > 1)
@require(lambda grid_size: grid_size % 2 == 1)
@ensure(lambda result: 0 <= result <= 1)
def simulate(trials: int, grid_size: int) -> float:
    """
    Simulate ``trials` number of wolf journeys on the quadratic ``grid_size`` grid."""
    success_count = 0

    half_grid_size = grid_size // 2
    border = (-half_grid_size, half_grid_size)

    for _ in range(trials):
        visited = set()  # type: Set[Position]

        position = Position(x=0, y=0)

        success = None  # type: Optional[bool]
        while True:
            assert position.x < half_grid_size, (
                f"position invariant for x: "
                f"{position=}, {half_grid_size=}, {grid_size=}"
            )
            assert position.y < half_grid_size, (
                f"position invariant for y: "
                f"{position=}, {half_grid_size=}, {grid_size=}"
            )
            assert (
                position not in visited
            ), f"visited invariant: {visited=}, {grid_size=}"

            old_visited_len = len(visited)
            visited.add(position)

            next_positions = list_next_positions(pos=position)

            if all(next_pos in visited for next_pos in next_positions):
                success = False
                break

            position = random.choice(
                [pos for pos in next_positions if pos not in visited]
            )
            if position.x in border or position.y in border:
                success = True
                break

            # ERROR (mristin, 2021-06-03):
            # The loop invariant is invalid. It should have been something like:
            # assert len(visited) == old_visited_len + 1, "Loop invariant"
            assert len(visited) == old_visited_len - 1, "Loop invariant"

        assert success is not None

        if success:
            success_count += 1

    return success_count / trials
