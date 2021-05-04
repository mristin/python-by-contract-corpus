"""
Consider two strings, ``s`` and ``t`` and a non-negative integer ``k``.

Check if the characters in ``t`` occur in ``s`` in an arbitrary order as a subsequence.
The distance between two matching characters from ``t`` in ``s`` must not be larger
than ``k``.

The distance between two characters is given as the number of characters in-between.
For example, the distance between the characters "a" and "b" in "a12345b" is 5.

Here are a couple of examples:

* ``s = "abbbc", t = "cab", k = 1``. The result is ``True``.
* ``s = "abbbbc", t = "cab", k = 1``. The result if ``False``. The distance between
  either "a" and "b" or "b" and "c" is larger than 1.
* ``s = "abc"

"""