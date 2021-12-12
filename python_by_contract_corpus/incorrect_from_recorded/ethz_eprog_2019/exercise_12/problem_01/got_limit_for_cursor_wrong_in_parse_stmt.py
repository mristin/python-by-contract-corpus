"""
Interpret mathematical programs developed in Exercise 11, Problem 1.

Instead of passing in the values for the expression evaluator, the variables are
assigned values in the program.

(We exclude the part of the problem related to implementing a REPL as handling the
user input/output is out-of-scope of this corpus.)

"""
# We copy/paste the solution from Exercise 11, Problem 02 and base this solution on it.
# In practical settings, the code would either live in the same place (so no separate
# modules) or we would refactor the common functionality to general tokenization and
# parsing modules, respectively.
#
# We opt for the former solution (all the code in the same module) for simplicity.
import abc
import enum
import io
import math
import re
from typing import (
    List,
    Pattern,
    Mapping,
    Union,
    Tuple,
    cast,
    Sequence,
    overload,
    Iterator,
    Generic,
    TypeVar,
    Set,
    MutableMapping,
)

from icontract import require, ensure, DBC

from python_by_contract_corpus import common


class TokenKind(enum.Enum):
    """Define the token."""

    NUM = 1  #: Number literal
    VAR = 2  #: Variable (or function) identifier
    OP = 4  #: Operator
    OPEN = 5  #: Opening parenthesis
    CLOSE = 6  #: Closing parenthesis
    WHITESPACE = 7  #: Whitespace (including tabs *etc.*)
    ASSIGN = 8  #: Assignment
    SEMICOLON = 9  #: Semicolon


class TokenizationRule:
    """Define a regular expression which specifies a token."""

    def __init__(self, kind: TokenKind, pattern: Pattern[str]) -> None:
        """Initialize with the given values."""
        self.kind = kind
        self.pattern = pattern

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.kind.value!r}, {self.pattern!r})"


TOKENIZATION = [
    TokenizationRule(
        TokenKind.NUM, re.compile(r"(inf|(0|[1-9][0-9]*)(\.[0-9]+)?(e[+\-]?[0-9]+)?)")
    ),
    TokenizationRule(TokenKind.VAR, re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")),
    TokenizationRule(TokenKind.OP, re.compile(r"[+\-*/^]")),
    TokenizationRule(TokenKind.OPEN, re.compile(r"\(")),
    TokenizationRule(TokenKind.CLOSE, re.compile(r"\)")),
    TokenizationRule(TokenKind.ASSIGN, re.compile(r"=")),
    TokenizationRule(TokenKind.SEMICOLON, re.compile(r";")),
    TokenizationRule(TokenKind.WHITESPACE, re.compile(r"\s+", re.M)),
]  #: Define rules so that we can map token kind 🠒 regular expression.

#: Map token kind 🠒 rule to be matched for that token kind.
TOKENIZATION_MAP = {
    rule.kind: rule for rule in TOKENIZATION
}  # type: Mapping[TokenKind, TokenizationRule]


class Token(DBC):
    """Represent a token of the source code."""

    # fmt: off
    @require(
        lambda value, kind:
        TOKENIZATION_MAP[kind].pattern.fullmatch(value)
    )
    @require(lambda value, start, end: len(value) == end - start)
    @require(lambda start, end: start < end)
    # fmt: on
    def __init__(self, value: str, start: int, end: int, kind: TokenKind) -> None:
        """Initialize with the given values."""
        self.value = value
        self.start = start
        self.end = end
        self.kind = kind

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on all the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Token):
            return (
                self.value == other.value
                and self.start == other.start
                and self.end == other.end
                and self.kind == other.kind
            )

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"{self.value!r}, {self.start}, {self.end}, {self.kind.value!r})"
        )


# fmt: off
@ensure(
    lambda text, result:
    tokens_to_text(result) == text  # type: ignore
)
@ensure(
    lambda text, result:
    all(
        token.value == text[token.start:token.end]
        for token in result
    ),
    "Token values correct"
)
@ensure(
    lambda result:
    all(
        token1.end == token2.start
        for token1, token2 in common.pairwise(result)
    ),
    "Tokens consecutive"
)
@ensure(
    lambda text, result:
    not (len(result) > 0)
    or result[-1].end == len(text),
    "Text tokenized till the end"
)
@ensure(
    lambda result:
    not (len(result) > 0)
    or result[0].start == 0,
    "Text tokenized from the start"
)
# fmt: on
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
                    Token(value=text[start:end], start=start, end=end, kind=rule.kind)
                )
                cursor = end
                break

        if old_cursor == cursor and cursor < len(text):
            raise SyntaxError(f"Unparsable source code at cursor {cursor}: {text!r}")

        assert cursor > old_cursor, f"Loop invariant; {cursor=}, {old_cursor=}"

    return result


@ensure(lambda tokens, result: tokens == tokenize(result))
def tokens_to_text(tokens: Sequence[Token]) -> str:
    """Serialize the ``tokens`` back into the original text."""
    return "".join(token.value for token in tokens)


class UnOp(enum.Enum):
    """Represent unary operators."""

    MINUS = "-"  #: Unary negative


# See precedence climbing,
# https://eli.thegreenplace.net/2012/08/02/parsing-expressions-by-precedence-climbing


class Associativity(enum.Enum):
    """Represent the associativity of a binary operator."""

    LEFT = "Left"  #: Left associative
    RIGHT = "Right"  #: Right associative


class BinOpInfo:
    """Specify precedence and associativity."""

    def __init__(self, precedence: int, associativity: Associativity) -> None:
        """Initialize with the given values."""
        self.precedence = precedence
        self.associativity = associativity


class BinOp(enum.Enum):
    """Represent binary operators."""

    ADD = "+"  #: Addition
    SUB = "-"  #: Subtraction
    MUL = "*"  #: Multiplication
    DIV = "/"  #: Division
    POW = "^"  #: Power


_STR_TO_BINOP = {literal.value: literal for literal in BinOp}

_BIN_OP_TABLE = {
    BinOp.ADD: BinOpInfo(precedence=1, associativity=Associativity.LEFT),
    BinOp.SUB: BinOpInfo(precedence=1, associativity=Associativity.LEFT),
    BinOp.MUL: BinOpInfo(precedence=2, associativity=Associativity.LEFT),
    BinOp.DIV: BinOpInfo(precedence=2, associativity=Associativity.LEFT),
    BinOp.POW: BinOpInfo(precedence=3, associativity=Associativity.RIGHT),
}

#: Express an identifier of a variable or a function.
IDENTIFIER_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9]*")


class Identifier(DBC, str):
    """Represent an identifier of a variable or of a function."""

    @require(lambda value: IDENTIFIER_RE.fullmatch(value))
    def __new__(cls, value: str) -> "Identifier":
        """Enforce the identifier properties on ``value``."""
        return cast(Identifier, value)


class Node(DBC):
    """Represent a node of an abstract syntax tree (AST) of a program."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        raise NotImplementedError()


class Expr(Node):
    """Represent a mathematical expression in an AST."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        raise NotImplementedError()


class Constant(Expr, DBC):
    """Represent a constant in AST."""

    @require(lambda value: value >= 0.0)
    @require(lambda value: not math.isnan(value))
    def __init__(self, value: float) -> None:
        """Initialize with the given values."""
        self.value = value

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Constant):
            return self.value == other.value

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.value})"


class Variable(Expr, DBC):
    """Represent a variable in the AST."""

    def __init__(self, identifier: Identifier) -> None:
        """Initialize with the given values."""
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Variable):
            return self.identifier == other.identifier

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.identifier!r})"


class UnaryOperation(Expr, DBC):
    """Represent an unary operation in the AST."""

    def __init__(self, target: "Expr", operator: UnOp) -> None:
        """Initialize with the given values."""
        self.target = target
        self.operator = operator

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, UnaryOperation):
            return self.target == other.target and self.operator == other.operator

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"{self.target!r}, operator={self.operator.value!r})"
        )


class BinaryOperation(Expr, DBC):
    """Represent a binary operation in the AST."""

    def __init__(self, left: "Expr", operator: BinOp, right: "Expr") -> None:
        """Initialize with the given values."""
        self.left = left
        self.operator = operator
        self.right = right

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, BinaryOperation):
            return (
                self.left == other.left
                and self.operator == other.operator
                and self.right == other.right
            )

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"{self.left!r}, {self.operator.value!r}, {self.right!r})"
        )


class Function(enum.Enum):
    """Enumerate the available functions."""

    SIN = "sin"  #: Sine
    COS = "cos"  #: Cosine
    TAN = "tan"  #: Tangent


_STR_TO_FUNCTION = {literal.value: literal for literal in Function}


class Call(Expr, DBC):
    """Represent a function call in the AST."""

    def __init__(self, function: Function, argument: "Expr") -> None:
        """Initialize with the given values."""
        self.function = function
        self.argument = argument

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Call):
            return self.function == other.function and self.argument == other.argument

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.function.value!r}, {self.argument!r})"


class Statement(Node):
    """Represent a statement in the AST."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        raise NotImplementedError()


class Assign(Statement):
    """Represent an assignment statement."""

    def __init__(self, target: Identifier, expr: Expr) -> None:
        """Initialize with the given values."""
        self.target = target
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Assign):
            return self.target == other.target and self.expr == other.expr

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.target!r}, {self.expr!r})"


class Program(Node, DBC):
    """Represent a parsed program."""

    def __init__(self, body: List[Statement]) -> None:
        """Initialize with the given values."""
        self.body = body

    def __eq__(self, other: object) -> bool:
        """
        Compare against ``other`` of the same class based on the properties.

        Otherwise, propagate to :py:attr:`object.__eq__`.
        """
        if isinstance(other, Program):
            return self.body == other.body

        return object.__eq__(self, other)

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.body!r})"


T = TypeVar("T")


class _Visitor(Generic[T]):
    def visit(self, node: Node) -> T:
        if isinstance(node, Constant):
            return self.visit_constant(node)
        elif isinstance(node, Variable):
            return self.visit_variable(node)
        elif isinstance(node, UnaryOperation):
            return self.visit_unary_operation(node)
        elif isinstance(node, BinaryOperation):
            return self.visit_binary_operation(node)
        elif isinstance(node, Call):
            return self.visit_call(node)
        elif isinstance(node, Assign):
            return self.visit_assign(node)
        elif isinstance(node, Program):
            return self.visit_program(node)
        else:
            raise NotImplementedError(repr(node))

    def visit_constant(self, node: Constant) -> T:
        return self.visit_default(node)

    def visit_variable(self, node: Variable) -> T:
        return self.visit_default(node)

    def visit_unary_operation(self, node: UnaryOperation) -> T:
        return self.visit_default(node)

    def visit_binary_operation(self, node: BinaryOperation) -> T:
        return self.visit_default(node)

    def visit_call(self, node: Call) -> T:
        return self.visit_default(node)

    def visit_assign(self, node: Assign) -> T:
        return self.visit_default(node)

    def visit_program(self, node: Program) -> T:
        return self.visit_program(node)

    def visit_default(self, node: Node) -> T:
        raise NotImplementedError(repr(node))


class TokensWoWhitespace(DBC):
    """Represent tokens without whitespace."""

    @require(lambda tokens: all(token.kind != TokenKind.WHITESPACE for token in tokens))
    def __new__(cls, tokens: Sequence[Token]) -> "TokensWoWhitespace":
        """Enforce the properties on ``tokens``."""
        return cast(TokensWoWhitespace, tokens)

    @overload
    def __getitem__(self, index: int) -> Token:
        """Get the token at the given integer index."""
        raise NotImplementedError("Only for type annotations")

    @overload
    def __getitem__(self, index: slice) -> "TokensWoWhitespace":
        """Get the slice of the tokens."""
        raise NotImplementedError("Only for type annotations")

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[Token, "TokensWoWhitespace"]:
        """Get the token(s) at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the tokens."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[Token]:
        """Iterate over the tokens."""
        raise NotImplementedError("Only for type annotations")


# fmt: off
@require(
    lambda tokens, cursor: 0 <= cursor < len(tokens),
    "Cursor not past end of source",
    error=SyntaxError,
    enabled=True
)
@ensure(lambda cursor, result: cursor < result[1], "Cursor moved")
# fmt: on
def _parse_atom(tokens: TokensWoWhitespace, cursor: int) -> Tuple[Expr, int]:
    remaining = len(tokens) - cursor

    if remaining >= 2 and tokens[cursor].value == "-":
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
                f"at column {tokens[cursor].start + 1}"
            )

        cursor += 1

        if identifier not in _STR_TO_FUNCTION:
            raise SyntaxError(f"Unexpected function: {identifier}")

        function = _STR_TO_FUNCTION[identifier]

        return Call(function=function, argument=argument), cursor

    elif remaining >= 1 and tokens[cursor].kind == TokenKind.VAR:
        atom = Variable(
            identifier=Identifier(tokens[cursor].value)
        )  # type: Union[Constant, Variable]
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
                f"at column {tokens[cursor].start + 1}"
            )

        cursor += 1

        return expr, cursor

    else:
        raise SyntaxError(
            f"Unexpected token {tokens[cursor].value!r} "
            f"of kind {tokens[cursor].kind!r} "
            f"at column {tokens[cursor].start + 1}; expected an atom"
        )


# fmt: off
@require(
    lambda tokens, cursor: 0 <= cursor < len(tokens),
    "Cursor not past end of source",
    error=SyntaxError,
    enabled=True
)
@require(lambda min_precedence: min_precedence >= 1)
@ensure(lambda cursor, result: cursor < result[1], "Cursor moved")
# fmt: on
def _parse_expr(
    tokens: TokensWoWhitespace, min_precedence: int, cursor: int
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
            tokens=tokens, min_precedence=next_min_precedence, cursor=cursor
        )

        atom_lhs = BinaryOperation(left=atom_lhs, operator=bin_op, right=atom_rhs)

    return atom_lhs, cursor


# fmt: off
@ensure(lambda cursor, result: cursor < result[1], "Cursor moved")
# fmt: on
def _parse_stmt(tokens: TokensWoWhitespace, cursor: int) -> Tuple[Statement, int]:
    """Parse a statement at the given ``cursor`` in the ``tokens``."""
    # ERROR (mristin, 2021-06-18):
    # I got the comparison wrong. It should have been something like:
    # if cursor >= len(tokens) - 3:
    #     raise SyntaxError(
    #         f"Expected at least four tokens for the assignment at cursor {cursor}, "
    #         f"but len(tokens) was {len(tokens)}: {tokens[cursor:]}"
    #     )
    if cursor < len(tokens) - 2:
        raise SyntaxError(
            f"Expected at least three tokens for the assignment at cursor {cursor}, "
            f"but len(tokens) was {len(tokens)}: {tokens[cursor:]}"
        )

    if tokens[cursor].kind != TokenKind.VAR:
        raise SyntaxError(
            f"Expected a variable as the assignment target, but got: {tokens[cursor]}"
        )

    target = Identifier(tokens[cursor].value)
    cursor += 1

    if tokens[cursor].kind != TokenKind.ASSIGN:
        raise SyntaxError(
            f"Expected an assignment ('=') at {cursor}, but got: {tokens[cursor]}"
        )
    cursor += 1

    expr, cursor = _parse_expr(tokens=tokens, min_precedence=1, cursor=cursor)

    if cursor >= len(tokens):
        raise SyntaxError(
            f"Expected a semi-colon (';') at {cursor}, but got end of input"
        )

    if tokens[cursor].kind != TokenKind.SEMICOLON:
        raise SyntaxError(
            f"Expected a semi-colon (';') at {cursor}, but got: {tokens[cursor]}"
        )
    cursor += 1

    return Assign(target=target, expr=expr), cursor


def parse_program(tokens: Sequence[Token]) -> Program:
    """Parse the given tokens into an abstract syntax tree of a program."""
    tokens_wo_ws = TokensWoWhitespace(
        [token for token in tokens if token.kind != TokenKind.WHITESPACE]
    )

    body = []  # type: List[Statement]

    cursor = 0
    while cursor < len(tokens_wo_ws):
        old_cursor = cursor

        stmt, cursor = _parse_stmt(tokens=tokens_wo_ws, cursor=cursor)
        body.append(stmt)

        assert old_cursor < cursor, f"Loop invariant: {cursor=}, {old_cursor=}"

    return Program(body=body)


class _UnparseVisitor(_Visitor[None]):
    """
    Generate the source code based on the abstract syntax tree of a program.

    The generated code is available through ``.code()``.
    """

    def __init__(self) -> None:
        self._writer = io.StringIO()

    def code(self) -> str:
        """Return the generated code."""
        return self._writer.getvalue()

    def visit_constant(self, node: Constant) -> None:
        self._writer.write(str(node.value))

    def visit_variable(self, node: Variable) -> None:
        self._writer.write(str(node.identifier))

    def visit_unary_operation(self, node: UnaryOperation) -> None:
        self._writer.write(str(node.operator.value))
        self._writer.write("(")
        self.visit(node.target)
        self._writer.write(")")

    def visit_binary_operation(self, node: BinaryOperation) -> None:
        self._writer.write("(")
        self.visit(node.left)
        self._writer.write(")")
        self._writer.write(str(node.operator.value))
        self._writer.write("(")
        self.visit(node.right)
        self._writer.write(")")

    def visit_call(self, node: Call) -> None:
        self._writer.write(str(node.function.value))
        self._writer.write("(")
        self.visit(node.argument)
        self._writer.write(")")

    def visit_assign(self, node: Assign) -> None:
        self._writer.write(f"{node.target} = ")
        self.visit(node.expr)
        self._writer.write(";")

    def visit_program(self, node: Program) -> None:
        for stmt in node.body:
            self.visit(stmt)
            self._writer.write("\n")

    def visit_default(self, node: Node) -> None:
        raise NotImplementedError(repr(node))


@ensure(lambda program, result: parse_program(tokenize(result)) == program)
def unparse(program: Program) -> str:
    """Convert the AST back to the source code."""
    visitor = _UnparseVisitor()
    visitor.visit(program)

    return visitor.code()


class _EvaluateVisitor(_Visitor[float]):
    """Visit the expressions and evaluate it."""

    @require(lambda lookup: all(IDENTIFIER_RE.fullmatch(key) for key in lookup.keys()))
    def __init__(self, lookup: Mapping[Identifier, float]):
        self.lookup = lookup

    def visit_constant(self, node: Constant) -> float:
        return node.value

    def visit_variable(self, node: Variable) -> float:
        value = self.lookup.get(node.identifier, None)
        if value is None:
            raise NameError(
                f"The variable {node.identifier} has not been provided a value."
            )

        return value

    def visit_unary_operation(self, node: UnaryOperation) -> float:
        target = self.visit(node.target)

        if node.operator == UnOp.MINUS:
            return -target
        else:
            raise NotImplementedError(repr(node))

    def visit_binary_operation(self, node: BinaryOperation) -> float:
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator == BinOp.ADD:
            return left + right

        elif node.operator == BinOp.SUB:
            return left - right

        elif node.operator == BinOp.MUL:
            return left * right

        elif node.operator == BinOp.DIV:
            return left / right

        elif node.operator == BinOp.POW:
            return left ** right

        else:
            raise NotImplementedError(repr(node))

    def visit_call(self, node: Call) -> float:
        argument = self.visit(node.argument)

        if node.function == Function.SIN:
            return math.sin(argument)
        elif node.function == Function.COS:
            return math.cos(argument)
        elif node.function == Function.TAN:
            return math.tan(argument)
        else:
            raise NotImplementedError(repr(node))

    def visit_default(self, node: Node) -> float:
        raise NotImplementedError(f"The node can not be evaluated: {node}")


def interpret(program: Program) -> Mapping[Identifier, float]:
    """Interpret the given program and return the values of the assigned variables."""
    variables = dict()  # type: MutableMapping[Identifier, float]
    for stmt in program.body:
        assert isinstance(stmt, Assign), f"Unexpected statement: {stmt=}"

        visitor = _EvaluateVisitor(lookup=variables)
        value = visitor.visit(stmt.expr)
        variables[stmt.target] = value

    return variables
