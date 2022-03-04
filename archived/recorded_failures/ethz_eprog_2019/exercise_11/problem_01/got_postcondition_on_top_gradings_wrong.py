"""
Analyze the grades of the students.

Here's an example of the data

.. code-block::

    111111004  5.0  5.0  6.0
    111111005  3.75 3.0  4.0
    111111006  4.5  2.25 4.0

Every line represents a grading of a student. It starts with her matriculation number,
followed by space-delimited grades (between 1.0 and 6.0, floats). The grades correspond
to lectures 1, 2 and 3, respectively.

Provide the function ``critical`` which accepts two arguments, ``bound1`` and
``bound2``. The function lists all the students which have "critical" grades.
A student should appear only once in the list.

A student is "critical" if the grade for the first lecture is smaller-equal ``bound1``
and the sum of the grades for the lecture 2 and 3 is smaller than ``bound2``.

On the above example, ``critical(4, 8)`` gives:

.. code-block::

    111111005

Provide the function ``top`` which lists the students with the best grades. The
parameter ``limit`` determines the number of the "top" students. If the number of
students is less than ``limit``, return the list of all the students.

A student should appear only once in the resulting list. The students are compared
based on the sum of the grades in all the three lectures. If the sum of grades is
equal for two students, the order in the list is undefined (*i.e.* does not matter).

On the above example, ``top(2)`` might return both the output:

.. code-block::

    111111004
    111111005

and:

.. code-block::

    111111004
    111111006

(Both outputs are valid.)

The parameter ``limit`` is always greater than 0. Both ``bound1`` and ``bound2`` are
expected in the range ``[0.0, 100.0]``.

"""
import math
from decimal import Decimal
import re
from typing import List, Pattern, AnyStr, cast, TypeVar, Iterable, Tuple, Optional

from icontract import require, ensure, DBC

from correct_programs.common import Lines

ALL_GRADES = [Decimal("0.25") * i for i in range(0, 25)]
ALL_GRADES_SET = set(ALL_GRADES)

# fmt: off
assert all(
    grade % 1 in (Decimal('0.0'), Decimal('0.25'), Decimal('0.5'), Decimal('0.75'))
    for grade in ALL_GRADES
)
# fmt: on
assert min(ALL_GRADES) == Decimal("0.0")
assert max(ALL_GRADES) == Decimal("6.0")


class Grade(DBC, Decimal):
    @require(lambda value: value in ALL_GRADES_SET)
    @require(lambda value: not value.is_nan())
    def __new__(cls, value: Decimal) -> "Grade":
        return cast(Grade, value)

    def __le__(self, other: "Grade") -> bool:
        return self < other

    def __add__(self, other: "Grade") -> Decimal:
        return self + other


class Grading:
    def __init__(
        self, identifier: str, grade1: Grade, grade2: Grade, grade3: Grade
    ) -> None:
        self.identifier = identifier
        self.grade1 = grade1
        self.grade2 = grade2
        self.grade3 = grade3

    @ensure(lambda result: result >= 0)
    def sum_grades(self) -> Decimal:
        return self.grade1 + self.grade2 + self.grade3


def compile_grading_re() -> Pattern[AnyStr]:
    id_re = "([a-zA-Z0-9]+)"

    grade_parts = []  # type: List[str]
    for grade in ALL_GRADES:
        if grade % 1 == Decimal("0.0"):
            grade_parts.append(f"{grade.normalize()}.0")
        else:
            grade_parts.append(str(grade.normalize()))

    grade_re = "".join(["("] + ["|".join(part for part in grade_parts)] + [")"])

    complete_re = f"^{id_re} +{grade_re} +{grade_re} +{grade_re}$"

    return re.compile(complete_re)  # type: ignore


GRADING_RE = compile_grading_re()


@require(lambda lines: all(GRADING_RE.match(line) for line in lines))
@ensure(
    lambda result: (
        identifiers := [grading.name for grading in result],
        len(identifiers) == len(set(identifiers)),
    )[1],
    "Unique identifiers",
)
@ensure(lambda lines, result: len(result) == len(lines))
def parse(lines: Lines) -> List[Grading]:
    result = []  # type: List[Grading]

    for line in lines:
        parts = [part for part in line.split(" ") if part.strip() != ""]
        assert len(parts) == 4, f"{parts=}"
        identifier = parts[0]
        grades = [Grade(Decimal(part)) for part in parts[1:]]

        result.append(
            Grading(
                identifier=identifier,
                grade1=grades[0],
                grade2=grades[1],
                grade3=grades[2],
            )
        )

    return result


# fmt: off
@require(
    lambda gradings:
    (
            identifiers := [grading.name for grading in gradings],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
@ensure(
    lambda result:
    (
            identifiers := [grading.name for grading in result],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
# fmt: on
def critical(gradings: List[Grading], bound1: Grade, bound2: Decimal) -> List[Grading]:
    result = []  # type: List[Grading]
    for grading in gradings:
        if grading.grade1 <= bound1 and grading.grade2 + grading.grade3 < bound2:
            result.append(grading)

    return result


# fmt: off
@require(
    lambda gradings:
    (
            identifiers := [grading.name for grading in gradings],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
@require(lambda limit: limit > 0)
@ensure(
    lambda result:
    (
            identifiers := [grading.name for grading in result],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
# ERROR:
# icontract.errors.ViolationError:
# len(result) == min(limit, len(gradings)):
# gradings was [<correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6A8C9CA0>, <correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6A8C9DF0>, <correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6B2F2580>]
# len(gradings) was 3
# len(result) was 3
# limit was 2
# min(limit, len(gradings)) was 2
# result was [<correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6A8C9CA0>, <correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6A8C9DF0>, <correct_programs.ethz_eprog_2019.exercise_11.problem_01.Grading object at 0x0000019A6B2F2580>]
#
# This case came from a unit test.
@ensure(
    lambda gradings, limit, result:
    len(result) == min(limit, len(gradings))
)
@ensure(
    lambda result:
    all(
        result[i].sum_grades() >= result[i + 1].sum_grades()
        for i in range(len(result) - 1)
    )
)
# fmt: on
def top(gradings: List[Grading], limit: int) -> List[Grading]:
    sorted_gradings = sorted(
        gradings, key=lambda grading: grading.sum_grades(), reverse=True
    )

    return sorted_gradings
