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
