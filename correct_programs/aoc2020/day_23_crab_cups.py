from icontract import DBC, ensure, require, snapshot
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
        """Add a new cup to the circle with ''label'',
        next to the current cup counter-clockwise."""
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
        """Check if ''label'' is present in the cup circle."""
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
        """Represent the cup circle using the labels of the cups."""
        return cup_circle_to_str(self)


# fmt: off
@require(lambda cup_labels: cup_labels.isdecimal())
@require(lambda cup_labels: len(set(cup_labels)) == len(cup_labels))
@ensure(lambda result, cup_labels: cup_labels == cup_circle_to_str(result))
# fmt: on
def initialize_cups(cup_labels: str) -> CupCircle:
    """Create a CupCircle from ''cup_labels''."""
    cup_circle = CupCircle()
    for label in cup_labels:
        cup_circle.add_new_cup(int(label))
    return cup_circle


# @ensure(lambda result, cup_circle: cup_circle == initialize_cups(result))
def cup_circle_to_str(cup_circle: CupCircle) -> str:
    """Return a string with the labels of the cups in ''cup_circle'',
    starting from the current cup."""
    result: List[str] = []
    if cup_circle.current_cup:
        tmp = cup_circle.current_cup
        result += str(tmp.label)
        while tmp.next_cup != cup_circle.current_cup:
            tmp = tmp.next_cup
            result += str(tmp.label)
    return "".join(result)


@snapshot(lambda cup_circle: len(str(cup_circle)), name="len_cup_circle")
@ensure(lambda OLD, cup_circle: OLD.len_cup_circle == len(str(cup_circle)))
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
@require(lambda cup_labels: cup_labels.isdecimal())
@require(lambda cup_labels: len(set(cup_labels)) == len(cup_labels))
# fmt: on
def solve_100_steps(cup_labels: str) -> CupCircle:
    """Solve the problem for 100 crab moves."""
    cup_circle = initialize_cups(cup_labels)
    for _ in range(100):
        crab_move(cup_circle)
    return cup_circle


# TODO remove
if __name__ == "__main__":
    print(solve_100_steps("389125467"))
