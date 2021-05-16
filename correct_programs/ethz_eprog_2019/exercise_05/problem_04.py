"""
Analyze the booking data of a hotel.

The data is given as:
* The room number,
* The beginning of the booking interval (as an integer, the day of year),
* Tne end of the booking interval (as an integer, the day of year),
* The price of the room per day,
* The price discount (as a floating point number between 0 and 100).

All bookings start and end in the same year.

The program answers the following questions:
* Which room was booked the most frequently? (as number of bookings)
* Which room was booked the longest (as number of days)
* Which room brought in the most revenue?
* What is the total revenue of the hotel for the year?
"""
import collections
from typing import MutableMapping, Collection

from icontract import require, ensure, DBC


class Entry(DBC):
    @require(lambda room_number: room_number > 0)
    @require(lambda start: 1 <= start <= 366)
    @require(lambda end: 1 <= end <= 366)
    @require(lambda start, end: start <= end)
    @require(lambda price_per_day: price_per_day > 0)
    @require(lambda price_discount: 0 <= price_discount <= 100)
    def __init__(
        self,
        room_number: int,
        start: int,
        end: int,
        price_per_day: float,
        price_discount: float,
    ) -> None:
        self.room_number = room_number
        self.start = start
        self.end = end
        self.price_per_day = price_per_day
        self.price_discount = price_discount

    @ensure(lambda result: result > 0)
    def duration(self) -> int:
        return self.end - self.start + 1


@require(lambda entries: len(entries) > 0)
@ensure(lambda entries, result: result in {entry.room_number for entry in entries})
def most_booked_room(entries: Collection[Entry]) -> int:
    histo = collections.defaultdict(lambda: 0)  # type: MutableMapping[int, int]
    for entry in entries:
        histo[entry.room_number] += 1

    return max(histo, key=lambda key: histo[key])


@require(lambda entries: len(entries) > 0)
@ensure(lambda entries, result: result in {entry.room_number for entry in entries})
def longest_booked_room(entries: Collection[Entry]) -> int:
    histo = collections.defaultdict(lambda: 0)  # type: MutableMapping[int, int]
    for entry in entries:
        histo[entry.room_number] += entry.duration()

    return max(histo, key=lambda key: histo[key])


@require(lambda entries: len(entries) > 0)
@ensure(lambda entries, result: result in {entry.room_number for entry in entries})
def room_with_most_revenue(entries: Collection[Entry]) -> int:
    histo = collections.defaultdict(lambda: 0)  # type: MutableMapping[int, float]
    for entry in entries:
        histo[entry.room_number] += (
            entry.duration() * entry.price_per_day * entry.price_discount
        )

    return max(histo, key=lambda key: histo[key])


@require(lambda entries: len(entries) > 0)
@ensure(lambda result: result >= 0)
def total_revenue(entries: Collection[Entry]) -> float:
    return sum(
        entry.duration() * entry.price_per_day * entry.price_discount
        for entry in entries
    )
