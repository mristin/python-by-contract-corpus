from collections import Counter
from itertools import combinations
from typing import List, Optional, Tuple

from icontract import require, ensure

@ensure(lambda result, total: result is None or result[0] + result[1] == total,
        "Returned items sum to the right total")
@ensure(lambda result, items: result is None or all(r in items for r in result),
        "Returned values appear in the input")
@ensure(
    lambda result, items: result is None
    or result[0] != result[1]
    or items.count(result[0]) > 1,
    "A duplicated result was produced from different input items"
)
def find_pair_with_sum(items: List[int], total: int) -> Optional[Tuple[int, int]]:
    for x in items:
        for y in items:
            # ERROR: x and y can be the same item
            if x + y == total:
                return (x, y)
    return None


