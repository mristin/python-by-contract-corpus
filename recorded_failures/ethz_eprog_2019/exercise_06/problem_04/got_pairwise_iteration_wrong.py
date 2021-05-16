"""
Implement a linked list which stores integers.

Provide the following operations:
* ``add_first``,
* ``remove_first``,
* ``remove_last``,
* ``clear``,
* ``is_empty``,
* ``get`` (at index),
* ``set`` (at index), and
* ``iterate`` (over all the elements of the list).

(We substantially shortened the text of this problem to only give the crux of the
problem and leave out the parts with user input/output. Please refer to the original
exercise in German for exact details.)
"""
from typing import Optional, Iterator
from icontract import require, ensure, invariant, snapshot, DBC


class Node:
    def __init__(self, value: int, next_node: Optional['Node']) -> None:
        self.value = value
        self.next_node = next_node


# fmt: off
@invariant(
    lambda self:
    self.is_empty() ^ (self._first is not None and self._last is not None)
)
@invariant(lambda self: len(list(self.iterate())) != 0 ^ self.is_empty())
@invariant(lambda self: self._last is None or self._last.next_node is None)
@invariant(lambda self: len(list(self.iterate())) == self.count())
# fmt: on
class LinkedList(DBC):
    def __init__(self) -> None:
        self._first = None  # type: Optional[Node]
        self._last = None  # type: Optional[Node]
        self._count = 0

    @snapshot(lambda self: self.count(), name="count")
    @snapshot(lambda self: list(self.iterate()), name="items")
    @ensure(lambda value, self, OLD: [value] + OLD.items == list(self.iterate()))
    @ensure(lambda self: not self.is_empty())
    @ensure(lambda self, OLD: self.count() == OLD.count + 1)
    def add_first(self, value: int) -> None:
        if self._first is None:
            self._first = Node(value=value, next_node=None)
            self._last = self._first
        else:
            self._first = Node(value=value, next_node=self._first)

        self._count += 1

    def count(self) -> int:
        return self._count

    @require(lambda self: not self.is_empty())
    @snapshot(lambda self: list(self.iterate()), name="items")
    @snapshot(lambda self: self.count(), name="count")
    @ensure(lambda self, OLD: OLD.items[1:] == list(self.iterate()))
    @ensure(lambda self, OLD: self.count() == OLD.count - 1)
    @ensure(lambda result, OLD: OLD.items[0] == result)
    def remove_first(self) -> int:
        value = self._first.value
        self._first = self._first.next_node
        self._count -= 1
        return value

    @require(lambda self: not self.is_empty())
    @snapshot(lambda self: self.count(), name="count")
    @snapshot(lambda self: list(self.iterate()), name="items")
    @ensure(lambda self, OLD: OLD.items[:-1] == list(self.iterate()))
    @ensure(lambda self, OLD: self.count() == OLD.count - 1)
    @ensure(lambda result, OLD: OLD.items[-1] == result)
    def remove_last(self) -> int:
        if self._first == self._last:
            self._count -= 1
            value = self._first.value
            self._first = None
            self._last = None
            return value

        cursor = self._first
        prev = None  # type: Optional[Node]
        while cursor != self._last:
            # ERROR (mristin):
            # I got the assignment of prev wrong, it should come befure cursor is
            # assigned to a new value.
            cursor = cursor.next_node
            prev = cursor

        value = self._last.value
        self._last = prev
        prev.next_node = None
        self._last = prev
        self._count -= 1
        return value

    @require(lambda self: not self.is_empty())
    @ensure(lambda self: self.is_empty())
    @ensure(lambda self: self.count() == 0)
    def clear(self) -> None:
        self._first = None
        self._last = None
        self._count = 0

    def is_empty(self) -> bool:
        return self._first is None

    @require(lambda self, index: 0 <= index < self.count())
    @ensure(lambda self, index, result: list(self.iterate())[index] == result)
    def get(self, index: int) -> int:
        cursor = self._first
        for _ in range(index):
            cursor = cursor.next_node

        return cursor.value

    @require(lambda self, index: 0 <= index < self.count())
    @ensure(lambda self, index, value: list(self.iterate())[index] == value)
    def set(self, index: int, value: int):
        cursor = self._first
        for _ in range(index):
            cursor = cursor.next_node

        cursor.value = value

    def iterate(self) -> Iterator[int]:
        cursor = self._first
        while cursor is not None:
            yield cursor.value
            cursor = cursor.next_node
