"""
Parse the time in Swiss german.

The time ``t`` is given in ``hh:mm`` (``hh`` for hours, ``mm`` for minutes). Translate
it to Swiss german.

The "Swiss time" goes only from 1 to 12, but different periods of the day are indicated
("znacht", "am morge" *etc.*). Here's the pattern:

.. code-block::

    00:00 -> 12i znacht
    01:45 -> viertel vor 2 znacht
    09:25 -> 5 vor halbi 10i am morge
    12:01 -> 1 ab 12i am mittag
    16:46 -> 14 vor 5i am namittag
    21:51 -> 9 vor 10i am abig
    22:37 -> 7 ab halbi 11i znacht

"Am morge" is before 12pm. 12pm is "mittag". "Namittag is till 6pm. "Abig" goes till
10pm. The remainder of the day is "znacht".

If the number of minutes (``mm``) is greater-equal 25 25, the hours are incremented by
1 ("5 vor halbi 10i").

If there are less than 25 minutes, you say "ab", but otherwise "vor". Between
the minutes 25 and 39, you say "vor halbi" or "ab halbi". If it is exactly 15, 30 or
45, you say "viertel ab", "halbi" or "viertel vor", respectively.

For the hours after 3, you need to put a suffix "i" ("viertel vor 2", but "1 ab 12i").
"""
