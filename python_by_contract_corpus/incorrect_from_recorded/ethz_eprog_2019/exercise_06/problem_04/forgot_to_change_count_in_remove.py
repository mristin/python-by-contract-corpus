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
from typing import Optional, Iterator, Iterable

from icontract import require, ensure, invariant, snapshot, DBC


class Node:
    """Represent a node of a linked list containing integers."""

    def __init__(self, value: int, next_node: Optional["Node"]) -> None:
        self.value = value
        self.next_node = next_node


def _values_except_node(linked_list: "LinkedList", node: Node) -> Iterator[int]:
    """Iterate over all the values of the ``linked_list`` and skip the ``node``."""
    if not linked_list.is_empty():
        cursor = Cursor(linked_list)
        while not cursor.done():
            if cursor._node is not node:
                yield cursor.value()

            cursor.move()


class Cursor:
    """Provide a cursor to iterate manually over a linked list."""

    def __init__(self, linked_list: "LinkedList") -> None:
        """Initialize the cursor to point to the beginning of the ``linked_list``."""
        self._node = linked_list._first
        self._previous = None  # type: Optional[Node]
        self._linked_list = linked_list

    @require(lambda self: not self.done())
    def value(self) -> int:
        """Retrieve the value point to by the cursor."""
        assert self._node is not None
        return self._node.value

    @require(lambda self: not self.done())
    def set_value(self, value: int) -> None:
        """Set the value in the linked list at the cursor."""
        assert self._node is not None
        self._node.value = value

    @require(lambda self: not self.done())
    def move(self) -> None:
        """Move the cursor to the next element."""
        assert self._node is not None
        self._previous = self._node
        self._node = self._node.next_node

    def done(self) -> bool:
        """Return ``True`` if the cursor is past the end of linked list."""
        return self._node is None

    def is_last(self) -> bool:
        """Return ``True`` if the cursor points to the last element of the list."""
        return self._node is self._linked_list._last

    # fmt: off
    @require(lambda self: not self.done())
    @snapshot(lambda self: self._linked_list.count(), name="count")
    @snapshot(
        lambda self:
        list(_values_except_node(self._linked_list, self._node)), name="values_without"
    )
    @ensure(lambda self, OLD: list(self._linked_list.values()) == OLD.values_without)
    # fmt: on
    def remove(self) -> int:
        """Remove the node (and the value, respectively) at the cursor."""
        assert self._node is not None
        value = self._node.value

        if self._linked_list.count() == 1:
            self._node = None
            self._linked_list._first = None
            self._linked_list._last = None
            # ERROR (mristin, 2021-05-24):
            # I forgot to update the count in the branch below.
            # self._linked_list._count = 0
            return value

        if self._previous is None:
            assert self._node == self._linked_list._first
            self._linked_list._first = self._node.next_node
            self._node = self._node.next_node
            self._linked_list._count -= 1
            return value

        self._previous.next_node = self._node.next_node

        if self._node == self._linked_list._last:
            self._linked_list._last = self._previous

        self._node = self._node.next_node

        self._linked_list._count -= 1

        return value


# fmt: off
@invariant(
    lambda self:
    self.is_empty() ^ (self._first is not None and self._last is not None)
)
@invariant(lambda self: len(list(self.values())) != 0 ^ self.is_empty())
@invariant(lambda self: self._last is None or self._last.next_node is None)
@invariant(lambda self: len(list(self.values())) == self.count())
# fmt: on
class LinkedList(DBC):
    """Provide a linked list."""

    def __init__(self, values: Optional[Iterable[int]] = None) -> None:
        """Initialize the list by populating it with the given ``values``."""
        self._first = None  # type: Optional[Node]
        self._last = None  # type: Optional[Node]
        self._count = 0

        if values is not None:
            for value in values:
                self.add_last(value)

    @snapshot(lambda self: self.count(), name="count")
    @snapshot(lambda self: list(self.values()), name="values")
    @ensure(lambda value, self, OLD: [value] + OLD.values == list(self.values()))
    @ensure(lambda self: not self.is_empty())
    @ensure(lambda self, OLD: self.count() == OLD.count + 1)
    def add_first(self, value: int) -> None:
        """Prepend the ``value`` to the list."""
        if self._first is None:
            self._first = Node(value=value, next_node=None)
            self._last = self._first
        else:
            self._first = Node(value=value, next_node=self._first)

        self._count += 1

    @snapshot(lambda self: self.count(), name="count")
    @snapshot(lambda self: list(self.values()), name="values")
    @ensure(lambda value, self, OLD: OLD.values + [value] == list(self.values()))
    @ensure(lambda self: not self.is_empty())
    @ensure(lambda self, OLD: self.count() == OLD.count + 1)
    def add_last(self, value: int) -> None:
        """Append the ``value`` to the list."""
        if self._first is None:
            self._first = Node(value=value, next_node=None)
            self._last = self._first
        else:
            assert self._last is not None

            old_last = self._last
            self._last = Node(value=value, next_node=None)
            old_last.next_node = self._last

        self._count += 1

    def count(self) -> int:
        return self._count

    @require(lambda self: not self.is_empty())
    @snapshot(lambda self: list(self.values()), name="values")
    @snapshot(lambda self: self.count(), name="count")
    @ensure(lambda self, OLD: OLD.values[1:] == list(self.values()))
    @ensure(lambda self, OLD: self.count() == OLD.count - 1)
    @ensure(lambda result, OLD: OLD.values[0] == result)
    def remove_first(self) -> int:
        """Remove first element of the list."""
        cur = Cursor(linked_list=self)
        return cur.remove()

    @require(lambda self: not self.is_empty())
    @snapshot(lambda self: self.count(), name="count")
    @snapshot(lambda self: list(self.values()), name="values")
    @ensure(lambda self, OLD: OLD.values[:-1] == list(self.values()))
    @ensure(lambda self, OLD: self.count() == OLD.count - 1)
    @ensure(lambda result, OLD: OLD.values[-1] == result)
    def remove_last(self) -> int:
        """Remove the last element of the list."""
        cur = Cursor(linked_list=self)
        while not cur.is_last():
            cur.move()

        return cur.remove()

    @require(lambda self: not self.is_empty())
    @ensure(lambda self: self.is_empty())
    @ensure(lambda self: self.count() == 0)
    def clear(self) -> None:
        """Remove all elements in the list."""
        self._first = None
        self._last = None
        self._count = 0

    def is_empty(self) -> bool:
        return self._first is None

    @require(lambda self, index: 0 <= index < self.count())
    @ensure(lambda self, index, result: list(self.values())[index] == result)
    def get(self, index: int) -> int:
        """Retrieve the ``index``-th element of the list."""
        cur = Cursor(linked_list=self)
        for _ in range(index):
            cur.move()

        return cur.value()

    @require(lambda self, index: 0 <= index < self.count())
    @ensure(lambda self, index, value: list(self.values())[index] == value)
    def set(self, index: int, value: int) -> None:
        """Set the ``index``-th element to ``value``."""
        cur = Cursor(linked_list=self)
        for _ in range(index):
            cur.move()

        cur.set_value(value)

    def values(self) -> Iterator[int]:
        """Iterate over all the values in the list."""
        cur = Cursor(linked_list=self)
        while not cur.done():
            yield cur.value()
            cur.move()

    def cursor(self) -> Cursor:
        """Get a cursor pointing to the beginning of the list."""
        return Cursor(linked_list=self)
