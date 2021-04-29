import collections
from typing import Final, Sequence, MutableMapping, Iterable, Tuple, TypeVar, Optional, \
    Mapping, cast, List

from icontract import require, ensure, DBC

T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """
    Iterate over ``(s0, s1, s2, ...)`` as ``((s0, s1), (s1, s2), ...)``.

    >>> list(pairwise([]))
    []

    >>> list(pairwise([1]))
    []

    >>> list(pairwise([1, 2]))
    [(1, 2)]

    >>> list(pairwise([1, 2, 3]))
    [(1, 2), (2, 3)]
    """
    previous = None  # type: Optional[T]
    for current in iterable:
        if previous is not None:
            yield previous, current

        previous = current


class HistogramOfDeltas(DBC, Mapping[int, int]):
    @require(lambda mapping: all(delta > 0 for delta in mapping.keys()))
    @require(lambda mapping: all(count >= 0 for count in mapping.values()))
    def __new__(cls, mapping: Mapping[int, int]) -> 'HistogramOfDeltas':
        return cast(HistogramOfDeltas, mapping)


# fmt: off
@require(lambda adapters: len(set(adapters)) == len(adapters))
@require(lambda adapters: all(adapter >= 0 for adapter in adapters))
# ERROR: missed the edge case when adapters are empty.
@ensure(
    lambda adapters, result: sum(result.values()) < len(adapters))
# fmt: on
def histogram_differences(adapters: List[int]) -> HistogramOfDeltas:
    histo = collections.defaultdict(lambda: 0)  # type: MutableMapping[int, int]

    for prev, current in pairwise(sorted(adapters)):
        delta = current - prev
        histo[delta] += 1

    return HistogramOfDeltas(histo)


@ensure(lambda result: result >= 0)
def compute_result(histo: HistogramOfDeltas) -> int:
    delta_1s = histo[1] if 1 in histo else 0
    delta_3s = histo[3] if 3 in histo else 0

    return delta_1s * delta_3s
