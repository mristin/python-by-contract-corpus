"""Provide common functionality shared among all the solutions."""

from typing import (
    Sequence,
    cast,
    overload,
    Union,
    Iterator,
    TypeVar,
    Iterable,
    Tuple,
    Optional,
)

from icontract import DBC, require


class Lines(DBC):
    """Represent a sequence of text lines."""

    # fmt: off
    @require(
        lambda lines:
        all('\n' not in line and '\r' not in line for line in lines)
    )
    # fmt: on
    def __new__(cls, lines: Sequence[str]) -> "Lines":
        r"""
        Ensure the properties on the ``lines``.

        Please make sure that you transfer the "ownership" immediately to Lines
        and don't modify the original list of strings any more:

        .. code-block:: python

            ##
            # OK
            ##

            lines = Lines(some_text.splitlines())

            ##
            # Not OK
            ##

            some_lines = some_text.splitlines()
            lines = Lines(some_lines)
            # ... do something assuming ``lines`` is immutable ...

            some_lines[0] = "This will break \n your logic"
            # ERROR! lines[0] now contains a new-line which is unexpected!

        """
        return cast(Lines, lines)

    def __add__(self, other: "Lines") -> "Lines":
        """Concatenate two list of lines."""
        raise NotImplementedError("Only for type annotations")

    # pylint: disable=function-redefined

    @overload
    def __getitem__(self, index: int) -> str:
        """Get the item at the given integer index."""
        pass

    @overload
    def __getitem__(self, index: slice) -> "Lines":
        """Get the slice of the lines."""
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[str, "Lines"]:
        """Get the line(s) at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the lines."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[str]:
        """Iterate over the lines."""
        raise NotImplementedError("Only for type annotations")


T = TypeVar("T")  # pylint: disable=invalid-name


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """
    Iterate over ``(s0, s1, s2, ...)`` as ``((s0, s1), (s1, s2), ...)``.

    >>> list(pairwise([]))
    []

    >>> list(pairwise([1]))
    []

    >>> list(pairwise([1, 2]))
    [(1, 2)]

    >>> list(pairwise([1, 2, 3]))
    [(1, 2), (2, 3)]
    """
    previous = None  # type: Optional[T]
    for current in iterable:
        if previous is not None:
            yield previous, current

        previous = current
