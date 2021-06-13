"""
Parse the file containing the list of bonus flying miles.

Here is an example:

.. code-block::

    Michaela Meier
    LX326 05.12.2016 ECONOMY
    LX317 10.01.2017 ECONOMY
    A3851 12.05.2017 BUSINESS
    LX8 12.10.2017 FIRST 4433
    .
    Stefan Oliver Schmid
    LX4150 19.10.2017 BUSINESS 6404
    .

The list consists of blocks. Each block begins with the name of the flier. The name
is then followed by the list of flights. For each flight, the flight number, the flight
date (in ``dd.mm.yyyy``), the class of the flight ("ECONOMY", "BUSINESS", "FIRST")
are given. If it is an inter-continental flight, the number of miles follows
the class of flight.

If no miles are given, you can assume a "flat-rate" of 125 miles. The miles flown in
"BUSINESS" are counted double and the miles in "FIRST" triple, respectively.

Output the number of miles per person.

For the aforementioned example:

.. code-block::

    Michaela Meier: 13799
    Stefan Oliver Schmid: 12808
"""
import datetime
import enum
import re
from typing import Mapping, List, Optional, MutableMapping, Pattern, AnyStr

from icontract import require, ensure, DBC

from correct_programs.common import Lines


class ClassOfFlight(enum.Enum):
    ECONOMY = "ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"


STR_TO_CLASS_OF_FLIGHT = {
    entry.value: entry for entry in ClassOfFlight
}  # type: Mapping[str, ClassOfFlight]


class Flight(DBC):
    @require(lambda miles: miles is None or miles > 0)
    @ensure(lambda miles, self: not (miles is None) or self.miles == 125)
    def __init__(
        self,
        number: str,
        date: datetime.date,
        class_of_flight: ClassOfFlight,
        miles: Optional[int],
    ) -> None:
        self.number = number
        self.date = date
        self.class_of_flight = class_of_flight
        self.miles = miles if miles is not None else 125


class Block(DBC):
    def __init__(self, name: str, flights: List[Flight]):
        self.name = name
        self.flights = flights


def compile_flight_re() -> Pattern[AnyStr]:
    number = r"(?P<number>[a-zA-Z0-9]+)"
    date = r"(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4})"
    class_of_flight = "".join(
        ["(?P<class_of_flight>"]
        + ["|".join(re.escape(enum_entry.value) for enum_entry in ClassOfFlight)]
        + [")"]
    )

    miles = r"( (?P<miles>[0-9]+))?"

    return re.compile(f"^{number} {date} {class_of_flight}{miles}$")  # type: ignore


FLIGHT_RE = compile_flight_re()


# fmt: off
@require(lambda lines: len(lines) >= 1)
@require(lambda lines: all(FLIGHT_RE.match(line) for line in lines[1:]))
@ensure(lambda lines, result: result.name == lines[0])
@ensure(
    lambda lines, result:
    not (len(lines) == 1) or len(result.flights) == 0
)
# fmt: on
def parse_block(lines: Lines) -> Block:
    name = lines[0]
    flights = []  # type: List[Flight]

    for line in lines[1:]:
        mtch = FLIGHT_RE.match(line)
        assert mtch

        flights.append(
            Flight(
                number=mtch.group("number"),
                date=datetime.datetime.strptime(mtch.group("date"), "%d.%m.%Y").date(),
                class_of_flight=STR_TO_CLASS_OF_FLIGHT[mtch.group("class_of_flight")],
                miles=None if mtch.group("miles") is None else int(mtch.group("miles")),
            )
        )

    return Block(name=name, flights=flights)


@ensure(lambda lines, result: not (len(lines) == 0) or len(result) == 0)
@ensure(lambda lines, result: not (len(lines) > 0) or len(result) > 0)
def parse(lines: Lines) -> List[Block]:
    list_of_block_lines = []  # type: List[Lines]

    accumulator = []  # type: List[str]
    for line in lines:
        if line == ".":
            if accumulator:
                list_of_block_lines.append(Lines(accumulator))
                accumulator = []
        else:
            accumulator.append(line)

    if accumulator:
        raise ValueError(
            "Unexpected unfinished block: {}".format("\n".join(accumulator))
        )

    return [parse_block(lines=block_lines) for block_lines in list_of_block_lines]


# fmt: off
@ensure(lambda result: all(value >= 0 for value in result.values()))
@ensure(
    lambda blocks, result:
    set(block.name for block in blocks) == set(result.keys()),
    "All people considered"
)
@ensure(
    lambda blocks, result:
    not (len(blocks) != 0) or len(result) > 0
)
# fmt: on
def compute_totals(blocks: List[Block]) -> MutableMapping[str, int]:
    result = dict()  # type: MutableMapping[str, int]

    for block in blocks:
        if block.name not in result:
            result[block.name] = 0

        for flight in block.flights:
            if flight.class_of_flight == ClassOfFlight.ECONOMY:
                result[block.name] += flight.miles
            elif flight.class_of_flight == ClassOfFlight.BUSINESS:
                result[block.name] += flight.miles * 2
            elif flight.class_of_flight == ClassOfFlight.FIRST:
                result[block.name] += flight.miles * 3
            else:
                raise NotImplementedError(flight.class_of_flight)

    return result
