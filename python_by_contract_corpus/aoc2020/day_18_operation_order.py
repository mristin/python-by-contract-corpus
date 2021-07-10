from enum import Enum
from typing import List, Union, Optional, cast
from dataclasses import dataclass
import regex as re
from icontract import require, ensure


NUMBER_RE = re.compile(r"^(-?\d+)")


class Operation(Enum):
    """Represent a mathematical operation."""

    ADD = "+"  #: Addition
    MUL = "*"  #: Multiplication


@dataclass(frozen=True)
class Tail:
    """Represent the tail of an expression."""

    op: Operation  #: Operation of the mathematical expression
    right: Union[int, "Node"]  #: Right-hand side of the expression


@dataclass(frozen=True)
class Node:
    """Represent a node of the abstract syntax tree of a mathematical expression."""

    head: Union[int, "Node"]  #: Constant or left-hand side expression
    tail: List[Tail]  #: Remaining expressions on the right-hand side


@require(lambda expr: re.match(r"^\(.+\)", expr))
@require(lambda expr: expr.count("(") == expr.count(")"))
@ensure(lambda expr, result: result in expr)
def extract_expression(expr: str) -> str:
    """Extract the sub-expression surrounded by parentheses in ``expr``."""
    parenthesis_balance = 0
    result = ""

    for c in expr:
        if c == "(":
            parenthesis_balance += 1
        elif c == ")":
            parenthesis_balance -= 1

        if parenthesis_balance == 0:
            return result[1:]
        else:
            result += c
    raise Exception("I should never end up here!")


def parse(expression: str) -> Optional[Node]:
    """Parse the ``expression`` into an abstract syntax tree."""
    if not expression:
        return None
    head: Union[int, Node]
    if expression.startswith("("):
        head_str = extract_expression(expression)
        assert parse(head_str) is not None
        head = cast(Node, parse(head_str))
        rest_expr = expression[len(head_str) + 2 :]
    elif NUMBER_RE.match(expression):
        head_str = NUMBER_RE.match(expression).group(1)
        head = int(head_str)
        rest_expr = expression[len(head_str) :]
    else:
        raise ValueError(f"Unexpected expression: {expression!r}")

    tails: List[Tail] = []

    while rest_expr:
        op = Operation(rest_expr[0])
        right: Union[int, Node]
        if rest_expr[1:].startswith("("):
            right_str = extract_expression(rest_expr[1:])
            assert parse(right_str) is not None
            right = cast(Node, parse(right_str))
            rest_expr = rest_expr[len(right_str) + 3 :]
        elif NUMBER_RE.match(rest_expr[1:]):
            right_str = NUMBER_RE.match(rest_expr[1:]).group(1)
            right = int(right_str)
            rest_expr = rest_expr[len(right_str) + 1 :]
        else:
            raise ValueError(f"Unexpected rest expression: {rest_expr}")

        tails.append(Tail(op=op, right=right))

    if not tails:
        return Node(head=head, tail=[])

    return Node(head=head, tail=tails)


@ensure(lambda result, node: parse(result) == node)
def serialize(node: Node) -> str:
    """Serialize the abstraction syntax tree given as ``node`` to a string."""
    result = ""
    if isinstance(node.head, int):
        result += str(node.head)
    else:
        result += "({})".format(serialize(node.head))

    if node.tail:
        for tail in node.tail:
            if isinstance(tail.right, int):
                result += "{}{}".format(tail.op.value, tail.right)
            else:
                result += "{}({})".format(tail.op.value, serialize(tail.right))

    return result


def compute(node: Node) -> int:
    """Evaluate the parsed expression given as ``node``."""
    if isinstance(node.head, int):
        result = node.head
    else:
        result = compute(node.head)

    for tail in node.tail:
        if isinstance(tail.right, int):
            right = tail.right
        else:
            right = compute(tail.right)

        if tail.op == Operation.ADD:
            result += right
        else:
            result *= right

    return result
