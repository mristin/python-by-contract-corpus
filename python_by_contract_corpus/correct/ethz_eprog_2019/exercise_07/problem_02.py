"""
Add an operation ``split`` to the linked list from Exercise 6, Problem 4.

The operation ``split`` takes in an argument ``n`` and removes all the items from the
list which are greater-equal ``n``.

The operation creates an additional list and inserts in it all the removed elements
(in the same order as in the original list). The resulting second list is finally
returned to the caller.

(The original problem statements includes an additional requirement that the caller
should be able to iterate over the original list by adding extra pointers ``old_next``
to the original nodes. We deliberately remove this part of the problem as it introduces,
in our opinion, complexity in the code with no or only marginal insights about
the nature of the code contracts).
"""
from typing import List

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_06.problem_04 import (
    LinkedList,
)

from icontract import require, ensure, snapshot


@require(lambda lst, old_values: len(lst) <= len(old_values))
def same_order(lst: List[int], old_values: List[int]) -> bool:
    """Check that the values in ``lst`` follow the order of the ``old_values``."""
    if len(lst) == 0:
        return True

    cur = 0
    for value in old_values:
        if value != lst[cur]:
            continue

        cur += 1
        if cur == len(lst):
            return True

    return cur == len(lst)


@snapshot(lambda lst: lst.count(), name="count")
@snapshot(lambda lst: list(lst.values()), name="values")
@ensure(lambda result, OLD: same_order(list(result.values()), OLD.values))
@ensure(lambda lst, OLD: same_order(list(lst.values()), OLD.values))
@ensure(lambda lst, n: all(value < n for value in lst.values()))
@ensure(lambda result, n: all(value >= n for value in result.values()))
@ensure(lambda lst, result, OLD: lst.count() + result.count() == OLD.count)
def split(lst: LinkedList, n: int) -> LinkedList:
    """
    Remove the elements greater-equal ``n`` from  the ``lst``.

     :return: The elements removed from the ``lst``
    """
    result = LinkedList()

    cursor = lst.cursor()

    while not cursor.done():
        value = cursor.value()
        if value >= n:
            result.add_last(value)
            cursor.remove()
        else:
            cursor.move()

    return result
