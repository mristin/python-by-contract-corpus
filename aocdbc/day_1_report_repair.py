from collections import Counter
from itertools import combinations
from typing import List, Optional, Tuple

from icontract import require, ensure

# Returned items sum to the right total
@ensure(lambda result, total: result is None or result[0] + result[1] == total)
# Returned values appear in the input
@ensure(lambda result, items: result is None or all(r in items for r in result))
# A duplicated result was produced from different input items
@ensure(
    lambda result, items: result is None
    or result[0] != result[1]
    or items.count(result[0]) > 1
)
def find_pair_with_sum(items: List[int], total: int) -> Optional[Tuple[int, int]]:
    for i, x in enumerate(items):
        for y in items[i + 1 :]:
            if x + y == total:
                return (x, y)
    return None


@require(lambda n: n >= 1)
# Correct number of items returned
@ensure(lambda result, n: result is None or len(result) == n)
# Returned items sum to the right total
@ensure(lambda result, total: result is None or sum(result) == total)
# Returned values appear in the input
@ensure(lambda result, items: result is None or all(i in items for i in result))
# We don't return duplicates that aren't also duplicated in the input
@ensure(lambda result, items: len(Counter(result) - Counter(items)) == 0)
def find_n_items_with_sum(
    items: List[int], n: int, total: int
) -> Optional[Tuple[int, ...]]:
    for combination in combinations(items, n):
        if sum(combination) == total:
            return combination
    return None
