from icontract import DBC, ensure, require, snapshot
import re
from typing import List, Optional


class Cup:
    """Represent a cup with a label and the cup next to it clockwise."""

    label: int  #: label of the cup
    next_cup: "Cup"  #: the next cup clockwise

    def __init__(self, label: int, next_cup: Optional["Cup"] = None) -> None:
        """Initialize with the given values."""
        self.label = label
        if next_cup:
            self.next_cup = next_cup
        else:
            self.next_cup = self


class CupCircle(DBC):
    """Represent a circle of cups as a circular linked list."""

    current_cup: Optional[Cup]  #: the cup from which each new move starts

    def __init__(self) -> None:
        """Initialize the circle as an empty circular linked list."""
        self.current_cup = None

    # fmt: off
    @require(lambda self, label: not self._is_label_in_circle(label))
    @require(lambda label: label >= 0)
    # fmt: on
    def add_new_cup(self, label: int) -> None:
        """
        Add a new cup to the circle with ``label``.

        The cup is added next to the current cup counter-clockwise.
        """
        if not self.current_cup:
            new_cup = Cup(label)
            new_cup.next_cup = new_cup
            self.current_cup = new_cup
        else:
            new_cup = Cup(label, self.current_cup)
            tmp = self.current_cup.next_cup
            while tmp.next_cup != self.current_cup:
                tmp = tmp.next_cup
            tmp.next_cup = new_cup

    def _is_label_in_circle(self, label: int) -> bool:
        """Check if ``label`` is present in the cup circle."""
        if not self.current_cup:
            return False
        tmp = self.current_cup
        while True:
            if label == tmp.label:
                return True
            tmp = tmp.next_cup
            if tmp == self.current_cup:
                break
        return False

    def __repr__(self) -> str:
        """Represent the circle as its labels."""
        return cup_circle_to_str(self)

    def __eq__(self, other: object) -> bool:
        """Return whether two circles are identical in the labels of the circle."""
        if isinstance(other, CupCircle):
            if self.current_cup and other.current_cup:
                tmp_1: Cup = self.current_cup
                tmp_2: Cup = other.current_cup
                while True:
                    if not tmp_1.label == tmp_2.label:
                        return False
                    tmp_1 = tmp_1.next_cup
                    tmp_2 = tmp_2.next_cup
                    if tmp_1 == self.current_cup or tmp_2 == other.current_cup:
                        if not tmp_1 == self.current_cup and tmp_2 == other.current_cup:
                            return False
                        return True
            if not (self.current_cup or other.current_cup):
                return True
            return False
        else:
            return object.__eq__(self, other)

    def __len__(self) -> int:
        """Return the number of cups in the circle."""
        if not self.current_cup:
            return 0
        length = 0
        tmp = self.current_cup
        while True:
            length += 1
            tmp = tmp.next_cup
            if tmp == self.current_cup:
                return length


NUMBER_RE = re.compile(r"[0-9]*")


@ensure(
    lambda result, cup_circle: cup_circle == initialize_cups(result)  # type: ignore
)
def cup_circle_to_str(cup_circle: CupCircle) -> str:
    """Stringify the labels of the ``cup_circle``, starting from the current cup."""
    result: List[str] = []
    if cup_circle.current_cup:
        tmp = cup_circle.current_cup
        result += str(tmp.label)
        while tmp.next_cup != cup_circle.current_cup:
            tmp = tmp.next_cup
            result += str(tmp.label)
    return "".join(result)


# fmt: off
@require(lambda cup_labels: NUMBER_RE.fullmatch(cup_labels))
@require(lambda cup_labels: len(set(cup_labels)) == len(cup_labels))
@ensure(lambda result, cup_labels: cup_labels == cup_circle_to_str(result))
# fmt: on
def initialize_cups(cup_labels: str) -> CupCircle:
    """Create a CupCircle from ``cup_labels``."""
    cup_circle = CupCircle()
    for label in cup_labels:
        cup_circle.add_new_cup(int(label))
    return cup_circle


@require(lambda cup_circle: len(cup_circle) >= 5)
@snapshot(lambda cup_circle: len(cup_circle), name="len_cup_circle")
@ensure(lambda OLD, cup_circle: OLD.len_cup_circle == len(cup_circle))
def crab_move(cup_circle: CupCircle) -> None:
    """Perform one move by the crab."""
    if not cup_circle.current_cup:
        raise Exception("the cup circle is empty")
    # 1. remove 3 cups clockwise from current cup
    removed_cups_head = cup_circle.current_cup.next_cup
    for _ in range(3):
        cup_circle.current_cup.next_cup = cup_circle.current_cup.next_cup.next_cup
    # 2. find destination cup
    destination_cup = None
    tmp = cup_circle.current_cup.next_cup
    while tmp != cup_circle.current_cup:
        if tmp.label < cup_circle.current_cup.label:
            if not destination_cup:
                destination_cup = tmp
            elif tmp.label > destination_cup.label:
                destination_cup = tmp
        tmp = tmp.next_cup
    if not destination_cup:
        tmp = cup_circle.current_cup.next_cup
        while tmp != cup_circle.current_cup:
            if not destination_cup:
                destination_cup = tmp
            elif tmp.label > destination_cup.label:
                destination_cup = tmp
            tmp = tmp.next_cup
        assert destination_cup
    # 3. place cups back
    removed_cups_head.next_cup.next_cup.next_cup = destination_cup.next_cup
    destination_cup.next_cup = removed_cups_head
    cup_circle.current_cup = cup_circle.current_cup.next_cup


# fmt: off
@require(lambda cup_labels: len(cup_labels) >= 5)
@require(lambda cup_labels: NUMBER_RE.fullmatch(cup_labels))
@require(lambda cup_labels: len(set(cup_labels)) == len(cup_labels))
@ensure(lambda result, cup_labels: len(cup_labels) == len(result))
# fmt: on
def solve_100_steps(cup_labels: str) -> CupCircle:
    """Solve the problem for 100 crab moves."""
    cup_circle = initialize_cups(cup_labels)
    for _ in range(100):
        crab_move(cup_circle)
    return cup_circle
