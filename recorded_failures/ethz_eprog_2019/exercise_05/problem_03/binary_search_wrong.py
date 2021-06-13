"""
Analyze the height data of a population.

The data is available at: http://jse.amstat.org/v11n2/datasets.heinz.html.

Given a series of measurements in centimeters, compute:
* The minimum, the maximum and average height of the population,
* A histogram of the heights given the number of bins
"""
import math
import statistics
from typing import Collection, Tuple, Sequence, cast, overload, Union, Iterator, List

from icontract import require, ensure, DBC, invariant

from correct_programs import common


class Measurements(DBC):
    @require(
        lambda values: all(0 < value < 400 for value in values),
        "Only valid values; the tallest man on earth ever measured was 251cm tall."
    )
    @require(lambda values: len(values) > 0)
    def __new__(cls, values: Sequence[float]) -> 'Measurements':
        return cast(Measurements, values)

    def __add__(self, other: "Measurements") -> "Measurements":
        """Concatenate two list of measurements."""
        raise NotImplementedError("Only for type annotations")

    # pylint: disable=function-redefined

    @overload
    def __getitem__(self, index: int) -> float:
        """Get the item at the given integer index."""
        pass

    @overload
    def __getitem__(self, index: slice) -> "Measurements":
        """Get the slice of the lines."""
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[float, "Measurements"]:
        """Get the line(s) at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the lines."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[float]:
        """Iterate over the lines."""
        raise NotImplementedError("Only for type annotations")


# fmt: off

@ensure(
    lambda result:
    len(set(result)) == len(result)
    and result[0] == result[1] == result[2],
    "Identical measurements all give the same min, average, max"
)
@ensure(
    lambda result:
    len(set(result)) != len(result)
    and result[0] < result[1] < result[2]
)
# fmt: on
def compute_stats(measurements: Measurements) -> Tuple[float, float, float]:
    return min(measurements), statistics.mean(measurements), max(measurements)


class Range:
    @require(lambda start, end: start < end)
    @require(lambda start: not math.isnan(start))
    @require(lambda end: not math.isnan(end))
    def __init__(self, start: float, end: float) -> None:
        self.start = start
        self.end = end


class BinRanges(DBC):
    # fmt: off
    @require(
        lambda lower_bound, upper_bound:
        lower_bound < upper_bound
    )
    @require(
        lambda upper_bound:
        not math.isnan(upper_bound) and not math.isinf(upper_bound)
    )
    @require(
        lambda lower_bound:
        not math.isnan(lower_bound) and not math.isinf(lower_bound)
    )
    @require(
        lambda lower_bound, upper_bound, bin_count:
        (
                bin_width := (upper_bound - lower_bound) / bin_count,
                bin_width != 0
        )[1],
        "Bin width not numerically zero"
    )
    @ensure(
        lambda result:
        all(
            previous.end == current.start
            for previous, current in common.pairwise(result)
        ),
        "Bin ranges without a hole"
    )
    @ensure(
        lambda bin_count, include_minus_inf, result:
        not (include_minus_inf ^ math.isinf(result[0].start)),
        "include_min_inf <=> lower bound of the first bin is -inf"
    )
    @ensure(
        lambda bin_count, include_inf, result:
        not (include_inf ^ math.isinf(result[-1].end)),
        "include_inf <=> upper bound of the last bin is +inf"
    )
    @ensure(
        lambda bin_count, include_inf, include_minus_inf, result:
        not (not include_inf and not include_minus_inf) or len(result) == bin_count,
        "bin_count does not refer to +/- inf bins"
    )
    @ensure(
        lambda bin_count, include_inf, include_minus_inf, result:
        not (include_inf and not include_minus_inf) or len(result) == bin_count + 1,
        "bin_count does not refer to +/- inf bins"
    )
    @ensure(
        lambda bin_count, include_inf, include_minus_inf, result:
        not (not include_inf and include_minus_inf) or len(result) == bin_count + 1,
        "bin_count does not refer to +/- inf bins"
    )
    @ensure(
        lambda bin_count, include_inf, include_minus_inf, result:
        not (include_inf and include_minus_inf) or len(result) == bin_count + 2,
        "bin_count does not refer to +/- inf bins"
    )
    # fmt: on
    def __new__(
            cls, bin_count: int, lower_bound: float, upper_bound: float,
            include_minus_inf: bool, include_inf: bool) -> 'BinRanges':
        ranges = []  # type: List[Range]

        if include_minus_inf:
            ranges.append(Range(start=-math.inf, end=lower_bound))

        bin_width = (upper_bound - lower_bound) / bin_count
        start = lower_bound
        for i in range(bin_count):
            end = start + bin_width

            # We need to account for numerical imprecision with summation
            # so that the last bin indeed matches the exact upper bound.
            if i < bin_count - 1:
                ranges.append(Range(start=start, end=end))
            else:
                ranges.append(Range(start=start, end=upper_bound))

            start = end

        if include_inf:
            ranges.append(Range(start=upper_bound, end=math.inf))

        return cast(BinRanges, ranges)

    @overload
    def __getitem__(self, index: int) -> Range:
        """Get the item at the given integer index."""
        pass

    @overload
    def __getitem__(self, index: slice) -> 'BinRanges':
        """Get the slice of the lines."""
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[Range, "BinRanges"]:
        """Get the line(s) at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the lines."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[Range]:
        """Iterate over the lines."""
        raise NotImplementedError("Only for type annotations")


# fmt: off
@require(lambda value: not math.isnan(value))
# ERROR:
# icontract.errors.ViolationError:
# Index not found or it corresponds to the correct bin range.: result == -1 or ranges[result].start <= value < ranges[result].end:
# ranges was [<problem_03.Range object at 0x000002612D18D1F0>, <problem_03.Range object at 0x000002612D18D5B0>, <problem_03.Range object at 0x000002612D18D3A0>, <problem_03.Range object at 0x000002612D18D670>, <problem_03.Range object at 0x000002612D18DB20>, <problem_03.Range object at 0x000002612D18DBB0>, <problem_03.Range object at 0x000002612D18DA90>, <problem_03.Range object at 0x000002612D18D550>, <problem_03.Range object at 0x000002612D18DF40>, <problem_03.Range object at 0x000002612D18DE20>, <problem_03.Range object at 0x000002612D18DAC0>, <problem_03.Range object at 0x000002612D18DFA0>]
# ranges[result].end was 1.2000000000000002
# ranges[result].start was 1.1
# result was 2
# value was 1.0
#
# Icontract-hypothesis on compute_histogram:
# Falsifying example: execute(
#     kwargs={'measurements': [1.0]},
# )
@ensure(
    lambda ranges, value, result:
    result == -1 or ranges[result].start <= value < ranges[result].end,
    "Index not found or it corresponds to the correct bin range"
)
@ensure(
    lambda ranges, value, result:
    not (ranges[0].start <= value <= ranges[-1].end) or 0 <= result < len(ranges),
    "Value in the ranges => bin found"
)
@ensure(
    lambda ranges, value, result:
    not (value > ranges[-1].end) or result == -1,
    "Value not covered in ranges => bin not found"
)
@ensure(
    lambda ranges, value, result:
    not (value < ranges[0].start) or result == -1,
    "Value not covered in ranges => bin not found"
)
# fmt: on
def bin_index(ranges: BinRanges, value: float) -> int:
    # Edge cases
    if value < ranges[0].start:
        return -1

    if value > ranges[-1].end:
        return -1

    if len(ranges) == 1:
        if ranges[0].start <= value < ranges[0].end:
            return 0
        else:
            return -1

    # Binary search
    first = 0
    last = len(ranges) - 1

    width = last - first + 1

    while True:
        # Cover the edge cases which are often coded wrong
        if last - first <= 2:
            if ranges[first].start <= value < ranges[first].end:
                return first

            return last

        middle = first + width // 2
        if ranges[middle].start <= value < ranges[middle].end:
            return middle

        if value < ranges[middle].start:
            last = middle - 1

        elif value > ranges[middle].end:
            first = middle + 1

        old_width = width
        width = last - first + 1
        assert width < old_width, "Loop invariant: the index range is getting smaller"


@invariant(lambda self: all(count >= 0 for count in self.counts))
class Histogram:
    @require(lambda ranges: len(ranges) > 0)
    def __init__(self, ranges: BinRanges) -> None:
        self.ranges = ranges
        self.counts = [0 for _ in range(len(ranges))]

    @require(lambda value: not math.isnan(value))
    @require(lambda self, value: self.ranges[0].start <= value < self.ranges[-1].end)
    def add(self, value: float) -> None:
        index = bin_index(self.ranges, value)
        assert 0 <= index < len(self.counts)

        self.counts[index] += 1

    def items(self) -> Iterator[Tuple[Range, int]]:
        assert len(self.ranges) == len(self.counts)
        return zip(self.ranges, self.counts)


# fmt: off
@ensure(
    lambda measurements, result:
    len(measurements) == sum(item[1] for item in result)
)
# fmt: on
def compute_histogram(measurements: Measurements) -> List[Tuple[Range, int]]:
    lower_bound = math.floor(min(measurements))
    upper_bound = math.ceil(max(measurements))

    if lower_bound == upper_bound:
        upper_bound += 1

    ranges = BinRanges(
        bin_count=10,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        include_minus_inf=True,
        include_inf=True
    )

    histogram = Histogram(ranges=ranges)

    for measurement in measurements:
        histogram.add(measurement)

    return list(histogram.items())
