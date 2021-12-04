import collections
import re
from typing import (
    MutableMapping,
    Mapping,
    cast,
    List,
    Iterator,
)

from icontract import require, ensure, DBC

from python_by_contract_corpus import common
from python_by_contract_corpus.common import Lines


class HistogramOfDeltas(DBC):
    """Represent a histogram of differences between adapters in jolts."""

    @require(lambda mapping: all(delta > 0 for delta in mapping.keys()))
    @require(lambda mapping: all(count >= 0 for count in mapping.values()))
    def __new__(cls, mapping: Mapping[int, int]) -> "HistogramOfDeltas":
        """Enforce histogram constraints."""
        return cast(HistogramOfDeltas, mapping)

    def __getitem__(self, key: int) -> int:
        """Retrieve the count corresponding to the histogram bin given with ``key``."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[int]:
        """Iterate over histogram bins."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Retrieve the number of the histogram bins."""
        raise NotImplementedError("Only for type annotations")


# fmt: off
@require(lambda adapters: len(set(adapters)) == len(adapters))
@require(lambda adapters: all(adapter >= 0 for adapter in adapters))
@require(
    lambda adapters: 0 not in adapters,
    "The charging input not in adapters")
# ERROR (mristin, 2021-04-29):
# Missed the edge case when adapters are empty in the pre-conditions; something like:
# @require(lambda adapters: len(adapters) > 0)
@ensure(
    lambda adapters, result:
    # Consider the charging output as 0 and the device input as max + 3
    sum(result.values()) == len(adapters) + 1
)
@ensure(
    lambda adapters, result:
    len(adapters) != 0 or sum(result.values()) == 0,
    "Empty histogram on empty input"
)
# fmt: on
def histogram_differences(adapters: List[int]) -> HistogramOfDeltas:
    """Compute the histogram of jolt differences in ``adapters``."""
    histo = collections.defaultdict(lambda: 0)  # type: MutableMapping[int, int]

    for prev, current in common.pairwise(sorted([0] + adapters + [max(adapters) + 3])):
        delta = current - prev
        histo[delta] += 1

    return HistogramOfDeltas(histo)


@ensure(lambda result: result >= 0)
def compute_result(histo: HistogramOfDeltas) -> int:
    """Analyze the histogram of jolt differences.

    :return: the product of the respective counts of 1s and 3s differences
    """
    delta_1s = histo[1] if 1 in histo else 0
    delta_3s = histo[3] if 3 in histo else 0

    return delta_1s * delta_3s


@require(lambda lines: all(re.match(r"^(0|[1-9][0-9]*)\Z", line) for line in lines))
@ensure(lambda lines, result: len(lines) == len(result))
def parse(lines: Lines) -> List[int]:
    """
    Parse the specification of the adapters given as ``lines``.

    :return: List of corresponding number of adapter jolts
    """
    return [int(line) for line in lines]
