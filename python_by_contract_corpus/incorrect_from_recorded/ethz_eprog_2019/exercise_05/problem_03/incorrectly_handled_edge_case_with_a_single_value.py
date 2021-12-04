"""
Analyze the height data of a population.

The data is available at: http://jse.amstat.org/v11n2/datasets.heinz.html.

Given a series of measurements in centimeters, compute:
* The minimum, the maximum and average height of the population,
* A histogram of the heights given the number of bins
"""
import math
import statistics
from typing import Tuple, Sequence, cast, overload, Union, Iterator, List

from icontract import require, ensure, DBC, invariant

from python_by_contract_corpus import common


class Measurement(DBC, float):
    """Represent a single measurement of a human height."""

    @require(
        lambda value: 0 < value < 400,
        "Only valid value; the tallest man on earth ever measured was 251cm tall.",
    )
    def __new__(cls, value: float) -> "Measurement":
        """Enforce the valid range on the measurement."""
        return cast(Measurement, value)


# fmt: off
@require(lambda measurements: len(measurements) > 0)
@ensure(
    lambda measurements, result:
    not (len(set(measurements)) == 1)
    or result[0] == result[1] == result[2],
    "Identical measurements all give the same min, average, max"
)
@ensure(
    lambda measurements, result:
    not (len(set(measurements)) != 1)
    or result[0] < result[1] < result[2]
)
# fmt: on
def compute_stats(measurements: List[Measurement]) -> Tuple[float, float, float]:
    """
    Compute the statistics of the given ``measurements``.

    :return: Minimum, mean, maximum
    """
    return min(measurements), statistics.mean(measurements), max(measurements)


class Range:
    """Represent a range of measurements."""

    @require(lambda start, end: start < end)
    @require(lambda start: not math.isnan(start))
    @require(lambda end: not math.isnan(end))
    def __init__(self, start: float, end: float) -> None:
        """Initialize with the given values."""
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        """Represent as mathematical range for easier debugging."""
        return f"[{self.start}, {self.end})"


class BinRanges(DBC):
    """Represent the ranges of the histogram bins."""

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
        cls,
        bin_count: int,
        lower_bound: float,
        upper_bound: float,
        include_minus_inf: bool,
        include_inf: bool,
    ) -> "BinRanges":
        """
        Construct ``bin_count`` number of histogram bins between ``lower_bound``
        and ``upper_bound``.

        If ``include_inf``, include -∞ and +∞ in the spanned total range of histogram.
        """
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
        """Get the bin range at the given integer index."""
        pass

    @overload
    def __getitem__(self, index: slice) -> "BinRanges":
        """Get the slice of the bin ranges."""
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[Range, "BinRanges"]:
        """Get the bin range at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the bin ranges."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[Range]:
        """Iterate over the bin ranges."""
        raise NotImplementedError("Only for type annotations")


# fmt: off
@require(lambda value: not math.isnan(value))
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
    """Find the index of the bin range among ``ranges`` corresponding to ``value``."""
    # Edge cases
    if value < ranges[0].start:
        return -1

    if value >= ranges[-1].end:
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
        if width <= 2:
            if ranges[first].start <= value < ranges[first].end:
                return first

            return last

        middle = first + width // 2
        if ranges[middle].start <= value < ranges[middle].end:
            return middle

        elif value < ranges[middle].start:
            last = middle - 1

        elif value >= ranges[middle].end:
            first = middle + 1

        else:
            raise AssertionError("Unexpected branch")

        old_width = width
        width = last - first + 1
        assert width < old_width, "Loop invariant: the index range is getting smaller"


@invariant(lambda self: all(count >= 0 for count in self.counts))
class Histogram(DBC):
    """Represent a mutable histogram."""

    @require(lambda ranges: len(ranges) > 0)
    def __init__(self, ranges: BinRanges) -> None:
        """Initialize the histogram with zero counts for ``ranges``."""
        self.ranges = ranges  #: Bin ranges

        #: Count of observations for the given bin
        self.counts = [0 for _ in range(len(ranges))]

    @require(lambda value: not math.isnan(value))
    @require(lambda self, value: self.ranges[0].start <= value < self.ranges[-1].end)
    def add(self, value: float) -> None:
        """Count the ``value`` in the corresponding bin."""
        index = bin_index(self.ranges, value)
        assert 0 <= index < len(self.counts)

        self.counts[index] += 1

    def items(self) -> Iterator[Tuple[Range, int]]:
        """Iterate over (bin range, count of observations)."""
        assert len(self.ranges) == len(self.counts)
        return zip(self.ranges, self.counts)


# fmt: off
@require(lambda measurements: len(measurements) > 0)
@ensure(
    lambda measurements, result:
    len(measurements) == sum(item[1] for item in result)
)
# fmt: on
def compute_histogram(measurements: Sequence[Measurement]) -> List[Tuple[Range, int]]:
    """
    Compute the histogram over ``measurements``.

    :return: List of (bin range, count of observations for that bin)
    """
    lower_bound = math.floor(min(measurements))
    upper_bound = math.ceil(max(measurements))

    if lower_bound == upper_bound:
        upper_bound += 1

    ranges = BinRanges(
        bin_count=10,
        # ERROR (mristin, 2021-05-16):
        # I forgot to replace the computations for lower and upper bound arguments
        # with the variables. Obviously, the variable ``upper_bound`` had to be changed
        # in case that there is a single measurement
        # (``if lower_bound == upper_bound: ...``), but this had no effect due to
        # the omission.
        lower_bound=math.floor(min(measurements)),
        upper_bound=math.ceil(max(measurements)),
        include_minus_inf=True,
        include_inf=True,
    )

    histogram = Histogram(ranges=ranges)

    for measurement in measurements:
        histogram.add(measurement)

    return list(histogram.items())
