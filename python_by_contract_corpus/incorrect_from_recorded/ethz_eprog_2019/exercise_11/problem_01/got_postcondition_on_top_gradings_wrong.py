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
import re
from decimal import Decimal
from numbers import Rational
from typing import List, cast, Union

from icontract import require, ensure, DBC

from python_by_contract_corpus.common import Lines

ALL_GRADES = [Decimal("0.25") * i for i in range(4, 25)]  #: List all possible grades.
ALL_GRADES_SET = set(ALL_GRADES)  #: Provide a set of all possible grades.

# fmt: off
assert all(
    grade % 1 in (Decimal('0.0'), Decimal('0.25'), Decimal('0.5'), Decimal('0.75'))
    for grade in ALL_GRADES
)
# fmt: on
MIN_GRADE = Decimal("1.0")
MAX_GRADE = Decimal("6.0")
assert min(ALL_GRADES) == MIN_GRADE
assert max(ALL_GRADES) == MAX_GRADE


class Grade(DBC, Decimal):
    """Represent a grade in Swiss educational system."""

    @require(lambda value: value in ALL_GRADES_SET)
    @require(lambda value: not value.is_nan())
    def __new__(cls, value: Decimal) -> "Grade":
        """Enforce the grade properties on ``value``."""
        return cast(Grade, value)

    def __le__(self, other: Union[Decimal, float, Rational, "Grade"]) -> bool:
        """Return ``True`` if ``self`` is smaller than ``other``."""
        return self < other

    def __add__(self, other: Union[Decimal, int, "Grade"]) -> Decimal:
        """Add ``self`` and ``other``."""
        return self + other


class Grading:
    """Represent the grading of a student."""

    def __init__(
        self, identifier: str, grade1: Grade, grade2: Grade, grade3: Grade
    ) -> None:
        """Initialize with the given values."""
        self.identifier = identifier
        self.grade1 = grade1
        self.grade2 = grade2
        self.grade3 = grade3

    @ensure(lambda result: 3 * MIN_GRADE <= result <= 3 * MAX_GRADE)
    def sum_grades(self) -> Decimal:
        """Sum all grades of the student."""
        return self.grade1 + self.grade2 + self.grade3


#: Express a grading entry for a student as a text.
#:
#: .. note::
#:
#:     The function :py:attr:`re.Pattern.__repr__` truncates at 200 characters
#:     so that the pattern in the docs (based on ``__repr__`` function) is possibly
#:     incorrect.
#:     See `Python issue #13592 <https://bugs.python.org/issue13592>`_.
GRADING_RE = re.compile(
    "([a-zA-Z0-9]+) +"
    "(1.0|1.25|1.5|1.75|2.0|2.25|2.5|2.75|3.0|3.25|3.5|3.75|4.0|"
    "4.25|4.5|4.75|5.0|5.25|5.5|5.75|6.0) +"
    "(1.0|1.25|1.5|1.75|2.0|2.25|2.5|2.75|3.0|3.25|3.5|3.75|4.0|"
    "4.25|4.5|4.75|5.0|5.25|5.5|5.75|6.0) +"
    "(1.0|1.25|1.5|1.75|2.0|2.25|2.5|2.75|3.0|3.25|3.5|3.75|4.0|"
    "4.25|4.5|4.75|5.0|5.25|5.5|5.75|6.0)"
)


@require(lambda lines: all(GRADING_RE.fullmatch(line) for line in lines))
@ensure(
    lambda result: (
        identifiers := [grading.identifier for grading in result],
        len(identifiers) == len(set(identifiers)),
    )[1],
    "Unique identifiers",
)
@ensure(lambda lines, result: len(result) == len(lines))
def parse(lines: Lines) -> List[Grading]:
    """Parse the grading entries given as ``lines``."""
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
            identifiers := [grading.identifier for grading in gradings],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
@ensure(
    lambda result:
    (
            identifiers := [grading.identifier for grading in result],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
# fmt: on
def critical(gradings: List[Grading], bound1: Grade, bound2: Decimal) -> List[Grading]:
    """
    List critical gradings among the ``gradings`` based on ``bound1`` and ``bound2``.

    Note that ``bound1`` and ``bound2`` have special semantics.
    Please consult the text of the problem.
    """
    result = []  # type: List[Grading]
    for grading in gradings:
        if grading.grade1 <= bound1 and grading.grade2 + grading.grade3 < bound2:
            result.append(grading)

    return result


# fmt: off
@require(
    lambda gradings:
    (
            identifiers := [grading.identifier for grading in gradings],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
@require(lambda limit: limit > 0)
@ensure(
    lambda result:
    (
            identifiers := [grading.identifier for grading in result],
            len(identifiers) == len(set(identifiers))
    )[1],
    "Students appear only once"
)
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
def top(
    gradings: List[Grading], limit: int  # pylint: disable=unused-argument
) -> List[Grading]:
    """Find the top ``limit`` students among the ``gradings``."""
    sorted_gradings = sorted(
        gradings, key=lambda grading: grading.sum_grades(), reverse=True
    )

    # ERROR (mristin, 2021-06-13):
    # I forgot to take only the top gradings, something like:
    # return sorted_gradings[:limit]
    return sorted_gradings
