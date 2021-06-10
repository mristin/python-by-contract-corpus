# pylint: disable

"""
Evaluate mathematical expressions.

Please see `page 3`_ and `page 4`_ of Exercise 11.

First, provide a tokenizer and a parser for the mathematical expressions.

Second, evaluate the mathematical expressions. The functions ``cos``, ``sin`` and
``tan`` need to be supported. The evaluation function is given a dictionary of parameter
values.

An exception should be raised if a parameter has not been specified.

.. _page 3: https://ethz.ch/content/dam/ethz/special-interest/infk/inst-cs/lst-dam/documents/Education/Classes/Fall2019/0027_Intro/Homework/u11.pdf?page=3
.. _page 4: https://ethz.ch/content/dam/ethz/special-interest/infk/inst-cs/lst-dam/documents/Education/Classes/Fall2019/0027_Intro/Homework/u11.pdf?page=4
"""
# pylint: enable
import enum
import math
import re
from typing import List, Pattern, AnyStr, Mapping, Union, Tuple, cast, Optional, \
    Sequence, overload, Iterator, Generic, TypeVar, Set

from icontract import require, ensure, DBC


class TokenKind(enum.Enum):
    """Define the token."""
    NUM = 1
    VAR = 2
    OP = 4
    OPEN = 5
    CLOSE = 6
    WHITESPACE = 7


class TokenizationRule:
    """Define a regular expression which specifies a token."""

    def __init__(self, kind: TokenKind, pattern: Pattern[AnyStr]) -> None:
        self.kind = kind
        self.pattern = pattern

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.kind.value!r}, {self.pattern!r})"


TOKENIZATION = [
    TokenizationRule(TokenKind.NUM, re.compile(r'(0|[1-9][0-9]*)(\.[0-9]+)?')),
    TokenizationRule(TokenKind.VAR, re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*')),
    TokenizationRule(TokenKind.OP, re.compile(r'[+\-*/^]')),
    TokenizationRule(TokenKind.OPEN, re.compile(r'\(')),
    TokenizationRule(TokenKind.CLOSE, re.compile(r'\)')),
    TokenizationRule(TokenKind.WHITESPACE, re.compile(r'\s+')),
]

TOKENIZATION_MAP = {
    rule.kind: rule
    for rule in TOKENIZATION
}  # type: Mapping[TokenKind, TokenizationRule]


class Token(DBC):
    """Represent a token of the source code."""

    @require(
        lambda text, start, end, kind:
        TOKENIZATION_MAP[kind].pattern.fullmatch(text[start:end])
    )
    @require(lambda text, end: 0 <= end <= len(text))
    @require(lambda text, start: 0 <= start < len(text))
    @require(lambda start, end: start < end)
    def __init__(
            self, text: str, start: int, end: int, kind: TokenKind
    ) -> None:
        self.text = text
        self.start = start
        self.end = end
        self.kind = kind

        self.value = self.text[self.start:self.end]

    def __eq__(self, other: 'Token') -> bool:
        return (
                self.text == other.text
                and self.start == other.start
                and self.end == other.end
                and self.kind == other.kind
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (f"{self.__class__.__name__}("
                f"{self.text!r}, {self.start}, {self.end}, {self.kind.value!r})")


@ensure(lambda text, result: tokens_to_text(result) == text)
def tokenize(text: str) -> List[Token]:
    """Tokenize the given ``text``."""
    if len(text) == 0:
        return []

    result = []  # type: List[Token]

    cursor = 0
    while cursor < len(text):
        old_cursor = cursor
        for rule in TOKENIZATION:
            mtch = rule.pattern.match(text, pos=cursor)
            if mtch:
                start, end = mtch.span()
                result.append(
                    Token(
                        text=text, start=start, end=end, kind=rule.kind))
                cursor = end
                break

        if old_cursor == cursor and cursor < len(text):
            raise SyntaxError(f"Unparsable source code: {text[cursor:cursor + 20]}")

        assert cursor > old_cursor, f"Loop invariant; {cursor=}, {old_cursor=}"

    return result


@ensure(lambda tokens, result: tokens == tokenize(result))
def tokens_to_text(tokens: Sequence[Token]) -> str:
    return ''.join(token.value for token in tokens)


class UnOp(enum.Enum):
    """Represent unary operators."""
    MINUS = "-"


# See precedence climbing,
# https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing

class Associativity(enum.Enum):
    LEFT = "Left"
    RIGHT = "Right"


class BinOpInfo:
    """Specify precedence and associativity."""

    def __init__(self, precedence: int, associativity: Associativity) -> None:
        self.precedence = precedence
        self.associativity = associativity


class BinOp(enum.Enum):
    """Represent binary operators."""
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "^"


_STR_TO_BINOP = {
    literal.value: literal
    for literal in BinOp
}

_BIN_OP_TABLE = {
    BinOp.ADD: BinOpInfo(precedence=1, associativity=Associativity.LEFT),
    BinOp.SUB: BinOpInfo(precedence=1, associativity=Associativity.LEFT),
    BinOp.MUL: BinOpInfo(precedence=2, associativity=Associativity.LEFT),
    BinOp.DIV: BinOpInfo(precedence=2, associativity=Associativity.LEFT),
    BinOp.POW: BinOpInfo(precedence=3, associativity=Associativity.RIGHT)
}

IDENTIFIER_RE = re.compile(r'[a-zA-Z_][a-zA-Z0-9]*')


class Identifier(DBC, str):
    """Represent an identifier of a variable or of a function."""

    @require(lambda value: IDENTIFIER_RE.fullmatch(value))
    def __new__(cls, value: str) -> 'Identifier':
        return cast(Identifier, value)


class Expr:
    """Represent a valid expression."""


class Constant(Expr, DBC):
    @require(lambda value: value >= 0.0)
    @require(lambda value: math.isnan(value))
    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Constant)
                and self.value == other.value
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.value})"


class Variable(Expr, DBC):
    def __init__(self, identifier: Identifier) -> None:
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Variable)
                and self.identifier == other.identifier
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.identifier!r})"


class UnaryOperation(Expr, DBC):
    def __init__(self, target: 'Expr', operator: UnOp) -> None:
        self.target = target
        self.operator = operator

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, UnaryOperation)
                and self.target == other.target
                and self.operator == other.operator
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"{self.target!r}, operator={self.operator.value!r})"
        )


class BinaryOperation(Expr, DBC):
    def __init__(self, left: 'Expr', operator: BinOp, right: 'Expr') -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, BinaryOperation)
                and self.left == other.left
                and self.operator == other.operator
                and self.right == other.right
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (f"{self.__class__.__name__}("
                f"{self.left!r}, {self.operator.value!r}, {self.right!r})")


class Call(Expr, DBC):
    """Represent a function call in the expression."""

    @require(lambda name: re.fullmatch(r'(sin|cos|tan)', name))
    def __init__(
            self, name: str, argument: 'Expr'
    ) -> None:
        self.name = name
        self.argument = argument

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Call)
                and self.name == other.name
                and self.argument == other.argument
        )

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.name!r}, {self.argument!r})"


T = TypeVar("T")


class _Visitor(Generic[T]):
    def visit(self, expr: Expr) -> T:
        if isinstance(expr, Constant):
            return self.visit_constant(expr)
        elif isinstance(expr, Variable):
            return self.visit_variable(expr)
        elif isinstance(expr, UnaryOperation):
            return self.visit_unary_operation(expr)
        elif isinstance(expr, BinaryOperation):
            return self.visit_binary_operation(expr)
        elif isinstance(expr, Call):
            return self.visit_call(expr)
        else:
            raise NotImplementedError(repr(expr))

    def visit_constant(self, expr: Constant) -> T:
        return self.visit_default(expr)

    def visit_variable(self, expr: Variable) -> T:
        return self.visit_default(expr)

    def visit_unary_operation(self, expr: UnaryOperation) -> T:
        return self.visit_default(expr)

    def visit_binary_operation(self, expr: BinaryOperation) -> T:
        return self.visit_default(expr)

    def visit_call(self, expr: Call) -> T:
        return self.visit_default(expr)

    def visit_default(self, expr: Expr) -> T:
        raise NotImplementedError(repr(expr))


class TokensWoWhitespace(DBC):
    """Represent tokens without whitespace."""

    @require(lambda tokens: all(token.kind != TokenKind.WHITESPACE for token in tokens))
    def __new__(cls, tokens: Sequence[Token]) -> "TokensWoWhitespace":
        return cast(TokensWoWhitespace, tokens)

    @overload
    def __getitem__(self, index: int) -> Token:
        pass

    @overload
    def __getitem__(self, index: slice) -> "TokensWoWhitespace":
        pass

    def __getitem__(
            self, index: Union[int, slice]
    ) -> Union[Token, "TokensWoWhitespace"]:
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[Token]:
        raise NotImplementedError("Only for type annotations")


@ensure(lambda cursor, result: cursor < result[1])
def _parse_atom(tokens: TokensWoWhitespace, cursor: int) -> Tuple[Expr, int]:
    if cursor >= len(tokens):
        raise SyntaxError("Unexpected end of source")

    remaining = len(tokens) - cursor

    if remaining >= 2 and tokens[cursor].value == '-':
        cursor += 1
        target, cursor = _parse_expr(tokens=tokens, min_precedence=1, cursor=cursor)

        return UnaryOperation(target=target, operator=UnOp.MINUS), cursor

    elif (
            remaining >= 2
            and tokens[cursor].kind == TokenKind.VAR
            and tokens[cursor + 1].kind == TokenKind.OPEN
    ):
        identifier = Identifier(tokens[cursor].value)
        cursor += 2

        argument, cursor = _parse_expr(tokens=tokens, min_precedence=1, cursor=cursor)

        if cursor >= len(tokens):
            raise SyntaxError("Unexpected end of source")

        if tokens[cursor].kind != TokenKind.CLOSE:
            raise SyntaxError(
                f"Unmatched '(', "
                f"got: {tokens[cursor].value!r} "
                f"at column {tokens[cursor].start + 1}")

        cursor += 1
        return Call(name=identifier, argument=argument), cursor

    elif remaining >= 1 and tokens[cursor].kind == TokenKind.VAR:
        atom = Variable(identifier=Identifier(tokens[cursor].value))
        cursor += 1

        return atom, cursor

    elif remaining >= 1 and tokens[cursor].kind == TokenKind.NUM:
        atom = Constant(value=float(tokens[cursor].value))
        cursor += 1

        return atom, cursor

    elif remaining >= 1 and tokens[cursor].kind == TokenKind.OPEN:
        cursor += 1
        expr, cursor = _parse_expr(tokens=tokens, min_precedence=1, cursor=cursor)

        if cursor >= len(tokens):
            raise SyntaxError("Unexpected end of source")

        if tokens[cursor].kind != TokenKind.CLOSE:
            raise SyntaxError(
                f"Unmatched '(', "
                f"got: {tokens[cursor].value!r} "
                f"at column {tokens[cursor].start + 1}")

        cursor += 1

        return expr, cursor

    else:
        raise SyntaxError(
            f"Unexpected token {tokens[cursor].value!r} "
            f"of kind {tokens[cursor].kind!r} "
            f"at column {tokens[cursor].start + 1}; expected an atom"
        )


@require(lambda min_precedence: min_precedence >= 1)
def _parse_expr(
        tokens: TokensWoWhitespace,
        min_precedence: int,
        cursor: int
) -> Tuple[Expr, int]:
    atom_lhs, cursor = _parse_atom(tokens=tokens, cursor=cursor)

    while True:
        if cursor >= len(tokens) or tokens[cursor].kind != TokenKind.OP:
            break

        bin_op = _STR_TO_BINOP[tokens[cursor].value]
        bin_op_info = _BIN_OP_TABLE[bin_op]

        if bin_op_info.precedence < min_precedence:
            break

        if bin_op_info.associativity == Associativity.LEFT:
            next_min_precedence = bin_op_info.precedence + 1
        else:
            next_min_precedence = bin_op_info.precedence

        cursor += 1

        atom_rhs, cursor = _parse_expr(
            tokens=tokens, min_precedence=next_min_precedence, cursor=cursor)

        atom_lhs = BinaryOperation(left=atom_lhs, operator=bin_op, right=atom_rhs)

    return atom_lhs, cursor


def parse_tokens(tokens: Sequence[Token]) -> Expr:
    """Parse the given tokens into an expression."""
    tokens_wo_ws = TokensWoWhitespace(
        [token for token in tokens if token.kind != TokenKind.WHITESPACE])

    expr, end = _parse_expr(tokens=tokens_wo_ws, min_precedence=1, cursor=0)

    if end != len(tokens_wo_ws):
        raise SyntaxError(
            f"Expected end of source, "
            f"but got token {tokens[end].value!r} "
            f"of kind {tokens[end].kind!r} "
            f"at column {tokens[end].start + 1}"
        )

    return expr


def _unparse(expr: Expr) -> List[str]:
    if isinstance(expr, Variable):
        return [expr.identifier]
    elif isinstance(expr, Constant):
        return [str(expr.value)]
    elif isinstance(expr, UnaryOperation):
        return (
                [expr.operator.value, '('] +
                _unparse(expr.target) +
                [')']
        )
    elif isinstance(expr, BinaryOperation):
        return (
                ['('] +
                _unparse(expr.left) +
                [')', expr.operator.value, '('] +
                _unparse(expr.right) +
                [')']
        )
    elif isinstance(expr, Call):
        return (
                [expr.name, '('] +
                _unparse(expr.argument)
                + [')']
        )
    else:
        raise AssertionError(str(expr))


@ensure(lambda expr, result: parse_tokens(tokenize(result)) == expr)
def unparse(expr: Expr) -> str:
    """Convert the AST to the source code."""
    parts = _unparse(expr)
    return ''.join(parts)


class _EvaluateVisitor(_Visitor[float]):
    """Visit the expressions and evaluate it."""

    @require(lambda lookup: all(IDENTIFIER_RE.fullmatch(key) for key in lookup.keys()))
    def __init__(self, lookup: Mapping[str, float]):
        self.lookup = lookup

    def visit_constant(self, expr: Constant) -> float:
        return expr.value

    def visit_variable(self, expr: Variable) -> float:
        return self.lookup[expr.identifier]

    def visit_unary_operation(self, expr: UnaryOperation) -> float:
        target = self.visit(expr.target)

        if expr.operator == UnOp.MINUS:
            return -target
        else:
            raise NotImplementedError(repr(expr))

    def visit_binary_operation(self, expr: BinaryOperation) -> float:
        left = self.visit(expr.left)
        right = self.visit(expr.right)

        if expr.operator == BinOp.ADD:
            return left + right

        elif expr.operator == BinOp.SUB:
            return left - right

        elif expr.operator == BinOp.MUL:
            return left * right

        elif expr.operator == BinOp.DIV:
            return left / right

        elif expr.operator == BinOp.POW:
            return left ** right

        else:
            raise NotImplementedError(repr(expr))

    def visit_call(self, expr: Call) -> float:
        argument = self.visit(expr.argument)

        if expr.name == 'sin':
            return math.sin(argument)
        elif expr.name == 'cos':
            return math.cos(argument)
        elif expr.name == 'tan':
            return math.tan(argument)
        else:
            raise NotImplementedError(repr(expr))


@require(lambda lookup: all(IDENTIFIER_RE.fullmatch(key) for key in lookup.keys()))
def evaluate(expr: Expr, lookup: Mapping[str, float]) -> float:
    """Evaluate the given expression substituting variables with ``lookup``."""
    visitor = _EvaluateVisitor(lookup=lookup)
    return visitor.visit(expr)


class _CollectVariablesVisitor(_Visitor[None]):
    """Collect all the variables from the expression."""

    def __init__(self) -> None:
        self.variable_set = set()  # type: Set[Identifier]

    def visit_constant(self, expr: Constant) -> None:
        pass

    def visit_variable(self, expr: Variable) -> None:
        self.variable_set.add(expr.identifier)

    def visit_unary_operation(self, expr: UnaryOperation) -> None:
        self.visit(expr.target)

    def visit_binary_operation(self, expr: BinaryOperation) -> None:
        self.visit(expr.left)
        self.visit(expr.right)

    def visit_call(self, expr: Call) -> None:
        self.visit(expr.argument)


def collect_variables(expr: Expr) -> Set[Identifier]:
    """Go recursively over the expression and collect the variable names."""
    visitor = _CollectVariablesVisitor()
    visitor.visit(expr)
    return visitor.variable_set

# ERROR:
# AssertionError: Smoke test for evaluation failed.
# problem_02.unparse(expr)='sin((-(A))^(-(A)))'
# lookup={'A': 0.8444218515250481}