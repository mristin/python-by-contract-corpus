from __future__ import annotations
from icontract import require, ensure, DBC
import re
from typing import Tuple, Optional, Union, List


class Computation(DBC):
    """
    Step 2: Validate
    Validation inherent to this class?
    """

    @require(lambda operators, operands: len(operators) + 1 == len(operands))
    @require(lambda operators: all(op in '+*' for op in operators))
    def __init__(self, operators: List[str], operands: List[Union[int, 'Computation']]):
        self.operators = operators
        self.operands = operands

    def compute(self) -> int:
        return compute(self)

    def __eq__(self, other):
        return self.operators == other.operators and \
               self.operators == other.operators


# TODO find a way to verify input
def parse(computation: str) -> Computation:
    """
    Step 1: Parse
    AST inspired: left, ops, comps
    What with the parentheses?
    """
    operators = []
    operands = []
    is_number = False
    nb_open_parentheses = 0
    number = ''
    sub_computation = ''
    for c in computation:

        assert not (number and sub_computation)

        if is_number and not c.isdigit():
            operands.append(int(number))
            number = ''
            is_number = False

        if c == ' ':
            pass
        elif nb_open_parentheses > 0:
            if c == ')':
                nb_open_parentheses -= 1
                if nb_open_parentheses > 0:
                    sub_computation += c
            else:
                if c == '(':
                    nb_open_parentheses += 1
                sub_computation += str(c)

            if nb_open_parentheses == 0:
                operands.append(parse(sub_computation))
                sub_computation = ''
        elif c == ')':
            raise Exception("not enough opening parentheses")
        elif c.isdigit():
            is_number = True
            number += str(c)
        elif c == '(':
            nb_open_parentheses += 1
        elif c in '+*':
            operators.append(c)
        else:
            raise Exception("unexpected character")

    assert not (number and sub_computation)

    if number:
        operands.append(int(number))
    elif sub_computation:
        operands.append(sub_computation)
    return Computation(operators, operands)


def compute(computation: Computation) -> int:
    """
    Step 3: Apply/compute
    """
    result = None
    operator = None
    for idx, operand in enumerate(computation.operands):
        if isinstance(operand, Computation):
            value = operand.compute()
        else:
            value = operand

        if not result:
            result = value
        else:
            if operator == '+':
                result += value
            else:
                result *= value
        if idx < len(computation.operands) - 1:
            operator = computation.operators[idx]
    return result
