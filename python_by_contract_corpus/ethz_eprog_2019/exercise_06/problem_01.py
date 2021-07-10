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

The period of day is determined as follows:

* "Am morge" is after 6am and before 12pm.
* 12pm is "mittag".
* "Namittag" is till 6pm.
* "Abig" goes till 10pm.
* The remainder of the day is "znacht".

If the number of minutes (``mm``) is greater-equal 25, the hours are incremented by
1 ("5 vor halbi 10i").

If there are less than 25 minutes, you say "ab", but otherwise "vor". Between
the minutes 25 and 39, you say "vor halbi" or "ab halbi". If it is exactly 15, 30 or
45, you say "viertel ab", "halbi" or "viertel vor", respectively.

For the hours after 3, you need to put a suffix "i" ("viertel vor 2", but "1 ab 12i").
"""

from icontract import require


@require(lambda hour: 0 <= hour < 23)
@require(lambda minute: 0 <= minute < 60)
def time_in_swiss_german(hour: int, minute: int) -> str:
    """Translate the given time of the day into Swiss german."""
    if hour < 6:
        period_of_day = "znacht"
    elif 6 <= hour < 12:
        period_of_day = "am morge"
    elif hour == 12:
        period_of_day = "am mittag"
    elif hour < 18:
        period_of_day = "am namittag"
    elif hour < 22:
        period_of_day = "am abig"
    else:
        period_of_day = "znacht"

    if hour == 0:
        clock_hour = 12
    elif hour > 12:
        clock_hour = hour - 12
    else:
        clock_hour = hour
    hour_suffix = "i" if clock_hour > 3 else ""

    if minute == 0:
        return f"{clock_hour}{hour_suffix} {period_of_day}"

    stated_hour = clock_hour if minute < 25 else clock_hour + 1

    if minute == 15:
        minute_part = "viertel ab"
    elif minute == 30:
        minute_part = "halbi"
    elif minute == 45:
        minute_part = "viertel vor"
    elif minute < 25:
        minute_part = f"{minute} ab"
    elif 25 <= minute < 30:
        minute_part = f"{30 - minute} vor halbi"
    elif 30 < minute <= 39:
        minute_part = f"{minute - 30} ab halbi"
    else:
        minute_part = f"{60 - minute} vor"

    result = f"{minute_part} {stated_hour}{hour_suffix} {period_of_day}"

    return result
