from icontract import ensure, require
import re
from typing import Set

# fmt: off
@require(
    lambda input_string: all(
        re.match(r"^[a-z]*$", line)
        for line in input_string.split("\n")
    )
)
@require(
    lambda input_string: all(
        len(set(list(line))) == len(line)
        for line in input_string.split("\n")
    )
)
@ensure(lambda result: result >= 0)
# fmt: on
def solve(input_string: str) -> int:
    """Count the number of yes answers in the group given as ``input_string``."""
    count = 0
    yes_answers: Set[str] = set()
    for line in input_string.split("\n"):
        if line:
            yes_answers = yes_answers.union(list(line))
        else:
            count += len(yes_answers)
            yes_answers.clear()
    count += len(yes_answers)
    return count
