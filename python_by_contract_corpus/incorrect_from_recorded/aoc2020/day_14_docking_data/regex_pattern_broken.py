import re
from typing import List, Mapping, MutableMapping, Tuple, Final

from icontract import require, ensure, DBC

# crosshair: on
from python_by_contract_corpus.common import Lines

MASK_RE = re.compile(r"^mask = (?P<mask>[01X]{36})\Z")


class Mask(DBC):
    """Represent the bitmask of the initialization program."""

    clearing: Final[int]  #: mask of the bits to be cleared (``AND``'ed)
    setting: Final[int]  #: mask of the bits to be set (``OR``'ed)

    @require(lambda clearing: 0 <= clearing <= 2**36 - 1)
    @require(lambda setting: 0 <= setting <= 2**36 - 1)
    def __init__(self, clearing: int, setting: int) -> None:
        """Initialize with the given values."""
        self.clearing = clearing
        self.setting = setting


@require(lambda text: MASK_RE.match(text))
@ensure(
    lambda result: 0 <= result.clearing <= 2**36 - 1,
    "The clearing mask not too large",
)
@ensure(
    lambda result: 0 <= result.setting <= 2**36 - 1, "The setting mask not too large"
)
def parse_mask(text: str) -> Mask:
    """Parse the text as an clearing and a setting mask, respectively."""
    mtch = MASK_RE.match(text)
    assert mtch is not None

    mask_text = mtch.group("mask")
    assert len(mask_text) == 36

    setting = 0
    clearing = 2**36 - 1

    # Loop from the least significant bit
    for bit_i in range(len(mask_text)):
        # ERROR (mristin, 2021-04-04):
        # I forgot to update the variable `text` to `mask_text` in the code.
        symbol = text[-bit_i - 1]
        if symbol == "0":
            clearing = clearing ^ (1 << bit_i)
        elif symbol == "1":
            setting = setting | (1 << bit_i)
        elif symbol == "X":
            pass
        else:
            raise NotImplementedError(f"{symbol=}")

    return Mask(clearing=clearing, setting=setting)


class Write(DBC):
    """Represent a write to the memory."""

    address: Final[int]  #: Address (offset) in the memory
    value: Final[int]  #: Value to be written

    @require(lambda address: address >= 0)
    @require(lambda value: 0 <= value <= 2**36 - 1, "The value in expected range")
    def __init__(self, address: int, value: int) -> None:
        """Initialize with the given values."""
        self.address = address
        self.value = value


WRITE_RE = re.compile(
    r"^mem\[(?P<address>0|[1-9][0-9]*)\] = (?P<value>0|[1-9][0-9]*)\Z"
)


@require(lambda text: WRITE_RE.match(text))
@ensure(lambda result: result[0] >= 0, "Address non-negative")
@ensure(lambda result: result[1] >= 0, "Value non-negative")
def parse_write(text: str) -> Tuple[int, int]:
    """Parse the write instruction and return (address, value)."""
    mtch = WRITE_RE.match(text)
    assert mtch is not None

    address = int(mtch.group("address"))
    value = int(mtch.group("value"))
    return address, value


class Program(DBC):
    """Represent the initialization program."""

    mask: Final[Mask]  #: Mask used throughout the program
    writes: Final[List[Write]]  #: Write instructions

    def __init__(self, mask: Mask, writes: List[Write]) -> None:
        """Initialize with the given values."""
        self.mask = mask
        self.writes = writes


@require(lambda lines: all(WRITE_RE.match(line) for line in lines[1:]))
@require(lambda lines: MASK_RE.match(lines[0]))
@require(lambda lines: len(lines) > 2)
def parse_lines(lines: Lines) -> Program:
    """Parse the input into an initialization program."""
    mask = parse_mask(text=lines[0])
    writes_as_tuples = [parse_write(line) for line in lines[1:]]

    for _, value in writes_as_tuples:
        if value >= 2**36:
            raise ValueError(f"Value does not fit in 35 bits (>= {2**36=}): {value}")

    writes = [
        Write(address=address, value=value) for address, value in writes_as_tuples
    ]

    return Program(mask=mask, writes=writes)


class Memory(DBC):
    """Represent the state of the memory."""

    slots: Final[Mapping[int, int]]  #: Slot map as address 🠒 value

    @require(
        lambda slots: all(value >= 0 for value in slots.values()), "Values non-negative"
    )
    @require(
        lambda slots: all(key >= 0 for key in slots.keys()), "Addresses non-negative"
    )
    def __init__(self, slots: Mapping[int, int]) -> None:
        """Initialize with the given values."""
        self.slots = slots


def execute(program: Program) -> Memory:
    """Execute the program and return the memory values."""
    slots = dict()  # type: MutableMapping[int, int]
    for write in program.writes:
        modified_value = (write.value | program.mask.setting) & program.mask.clearing
        slots[write.address] = modified_value

    return Memory(slots=slots)


@ensure(lambda result: result >= 0)
def sum_memory(memory: Memory) -> int:
    """Sum the values in the memory slots."""
    return sum(memory.slots.values())
