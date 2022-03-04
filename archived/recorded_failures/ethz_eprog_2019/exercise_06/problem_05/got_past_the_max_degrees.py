"""
Compute the angles of the clock hands for a given time of the day.

The 00:00:00 corresponds to the angle zero, increasing to the right. (This was *not*
part of the original problem statement, but we introduce it here for simplicity of the
solution.)

(We change slightly the statement so that it focuses on what we thought the "core" part
of the problem. The original problem additionally concerns the drawing of the clock
hands in the GUI which we intentionally leave out as Java-specific and not relevant
in terms of contracts.)
"""
from typing import Tuple

from icontract import require, ensure

# fmt: off
@require(lambda hour: 0 <= hour <= 23)
@require(lambda minute: 0 <= minute < 60)
@require(lambda second: 0 <= second < 60)
# ERROR:
# Falsifying example: execute(
#     kwargs={'hour': 12, 'minute': 1, 'second': 1},
# )
#
# icontract.errors.ViolationError:
# all(0 <= angle < 360 for angle in result):
# all(0 <= angle < 360 for angle in result) was False, e.g., with
#   angle = 360.5083333333333
# result was (360.5083333333333, 6.1, 6.0)
@ensure(lambda result: all(0 <= angle < 360 for angle in result))
@ensure(
    lambda hour, minute, second, result:
    not (hour == 0 and minute == 0 and second == 0)
    or result[0] == 0 and result[1] == 0 and result[2] == 0,
    "Angles start from 00:00:00")
@ensure(
    lambda hour, minute, second, result:
    not (hour == 0 and minute == 0 and second > 0)
    or result[0] > 0 and result[1] > 0 and result[2] > 0,
    "All hands of a clock move when the hand for seconds moves"
)
@ensure(
    lambda hour, result: hour / 12 * 360 <= result[0] < (hour + 1) / 12 * 360,
    "Hour hand between two hour ticks"
)
@ensure(
    lambda minute, result: minute / 60 * 360 <= result[1] < (minute + 1) / 60 * 360,
    "Minute hand between two minute ticks"
)
@ensure(
    lambda second, result: second / 60 * 360 <= result[2] < (second + 1) / 60 * 360,
    "Second hand between two second ticks"
)
@ensure(
    lambda hour, minute, second, result:
    not (minute == 0 and second == 0)
    or result[0] == hour / 12 * 360 and result[1] == 0 and result[2] == 0
)
# fmt: on
def compute_angles(hour: int, minute: int, second: int) -> Tuple[float, float, float]:
    angle_second = second / 60 * 360

    angle_minute = (minute + second / 60) / 60 * 360

    angle_hour = (hour + minute / 60 + second / 3600) / 12 * 360

    return angle_hour, angle_minute, angle_second
