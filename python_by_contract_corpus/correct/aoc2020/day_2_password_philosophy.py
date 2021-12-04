import re
from typing import Optional

from icontract import require, ensure

ENTRY_RE = re.compile(
    r"^(?P<min_count>[1-9][0-9]*)-(?P<max_count>[1-9][0-9]*) "
    r"(?P<character>[a-z]): (?P<password>[a-z]+)$"
)


@require(lambda line: ENTRY_RE.match(line))
def verify_line(line: str) -> Optional[bool]:
    """Verify an entry of the password database."""
    # crosshair: on
    mtch = ENTRY_RE.match(line)
    assert mtch is not None

    min_count = int(mtch.group("min_count"))
    max_count = int(mtch.group("max_count"))
    character = mtch.group("character")
    password = mtch.group("password")

    if min_count > max_count:
        return None

    return verify(
        min_count=min_count,
        max_count=max_count,
        character=character,
        password=password,
    )


@require(lambda min_count: min_count > 0)
@require(lambda max_count: max_count > 0)
@require(lambda min_count, max_count: min_count <= max_count)
@require(lambda character: len(character) == 1)
@ensure(lambda password, result: not (len(password) == 0) or not result)
def verify(min_count: int, max_count: int, character: str, password: str) -> bool:
    """Verify the ``password`` under the given constraints."""
    # crosshair: on
    answer = min_count <= password.count(character) <= max_count
    return answer
