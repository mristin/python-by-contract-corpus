import abc
import re
from typing import (
    List,
    Mapping,
    MutableMapping,
    Tuple,
    Optional,
    Dict,
    TypeVar,
    Generic,
    Final,
    Iterator,
)

from icontract import require, ensure, DBC

# crosshair: on
from python_by_contract_corpus.common import Lines


class Rule(DBC):
    """Represent a rule that valid messages should obey."""

    # fmt: off
    @ensure(
        lambda text, result:
        not (result is not None)
        or (len(text) > len(result))
    )
    @ensure(
        lambda text, result:
        not (result is not None) or (text.endswith(result))
    )
    @abc.abstractmethod
    # fmt: on
    def match(self, text: str) -> Optional[str]:
        """
        Match the ``text`` and return the remaining unmatched text.

        If the beginning of the ``text`` does not match, return ``None``.
        """
        raise NotImplementedError()


class RuleOr(Rule):
    """Represent an union composition of rules (at least one rule matches)."""

    rules: Final[List[Rule]]  #: Union of rules

    def __init__(self, rules: List[Rule]) -> None:
        """Initialize with the given values."""
        self.rules = rules

    def match(self, text: str) -> Optional[str]:
        """Check whether at least one rule from :py:attr:`rules` matches."""
        for rule in self.rules:
            remaining_suffix = rule.match(text)
            if remaining_suffix is not None:
                return remaining_suffix

        return None


class RuleSequence(Rule):
    """Represent a chain of rules where all rules need to match in sequence."""

    rules: Final[List[Rule]]  #: Rule chain

    def __init__(self, rules: List[Rule]) -> None:
        """Initialize with the given values."""
        self.rules = rules

    def match(self, text: str) -> Optional[str]:
        """Check whether ``text`` matches the whole sequence of :py:attr:`rules`."""
        remaining = text  # type: Optional[str]
        for rule in self.rules:
            assert remaining is not None
            remaining = rule.match(text=remaining)
            if remaining is None:
                return None

        return remaining


class RuleLiteral(Rule):
    """Represent a rule where a literal is exactly matched."""

    literal: Final[str]  #: Literal to be matched

    def __init__(self, literal: str) -> None:
        """Initialize with the given values."""
        self.literal = literal

    # fmt: off
    @ensure(
        lambda self, text, result:
        not (result is not None) or (self.literal + result == text)
    )
    # fmt: on
    def match(self, text: str) -> Optional[str]:
        """Check whether ``text`` matches exactly the :py:attr:`literal`."""
        if not text.startswith(self.literal):
            return None

        return text[len(self.literal) :]


class Node(DBC):
    """Represent a node in the abstract syntax tree."""

    pass


class NodeLiteral(Node):
    """Represent a literal in the rule syntax."""

    literal: Final[str]  #: Parsed literal

    def __init__(self, literal: str) -> None:
        """Initialize with the given values."""
        self.literal = literal


class NodeReference(Node):
    """Represent a reference to a rule."""

    identifier: Final[int]  #: Identifier of the referenced rule

    def __init__(self, identifier: int) -> None:
        """Initialize with the given values."""
        self.identifier = identifier


class NodeSequence(Node):
    """Represent a parsed sequence of node references."""

    references: Final[List[NodeReference]]  #: Parsed references

    def __init__(self, references: List[NodeReference]) -> None:
        """Initialize with the given values."""
        self.references = references


class NodeOr(Node):
    """Represent a parsed union of node sequences."""

    sequences: Final[List[NodeSequence]]  #: Union

    def __init__(self, sequences: List[NodeSequence]) -> None:
        """Initialize with the given values."""
        self.sequences = sequences


RULE_RE = re.compile(
    r"^"
    r"(?P<identifier>0|[1-9][0-9]*): "
    r"(?P<body>"
    r'"([^"]*)"'
    r"|"
    r"(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*"
    r"( \| (0|[1-9][0-9]*)( (0|[1-9][0-9]*))*)*"
    r")\Z"
)

RULE_LITERAL_RE = re.compile(r'^"(?P<literal>[^"]*)"\Z')
RULE_COMPOSITE_RE = re.compile(
    r"^(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*"
    r"( \| (0|[1-9][0-9]*)( (0|[1-9][0-9]*))*)*\Z"
)


@require(lambda line: RULE_RE.match(line))
def parse_rule(line: str) -> Tuple[int, Node]:
    """Parse the rule from the ``line`` into (rule identifier, abstract syntax tree)."""
    mtch = RULE_RE.match(line)
    assert mtch is not None

    identifier = int(mtch.group("identifier"))

    body = mtch.group("body")

    mtch = RULE_LITERAL_RE.match(body)
    if mtch:
        node = NodeLiteral(literal=mtch.group("literal"))  # type: Node
        return identifier, node

    mtch = RULE_COMPOSITE_RE.match(body)
    if mtch:
        texts_of_sequences = body.split(" | ")
        sequences = []  # type: List[NodeSequence]

        for text_of_sequence in texts_of_sequences:
            references = [
                NodeReference(identifier=int(reference_text))
                for reference_text in text_of_sequence.split(" ")
            ]

            sequences.append(NodeSequence(references=references))

        # Optimize for nicer representation
        if len(sequences) == 1:
            return identifier, sequences[0]
        else:
            node = NodeOr(sequences=sequences)
            return identifier, node

    raise NotImplementedError(
        f"The body {body!r} of a rule could not be parsed: {line!r}"
    )


@require(lambda lines: all(RULE_RE.match(line) for line in lines))
def parse_rules(lines: Lines) -> MutableMapping[int, Node]:
    """Parse the rules from ``lines`` into a dictionary of identifier 🠒 AST."""
    rule_trees = dict()  # type: Dict[int, Node]

    for line in lines:
        identifier, node = parse_rule(line=line)
        rule_trees[identifier] = node

    return rule_trees


T = TypeVar("T")


class _AbstractVisitor(abc.ABC, Generic[T]):
    """Structure a general visitor to an abstract syntax tree of rules."""

    @abc.abstractmethod
    def visit_literal(self, node: NodeLiteral) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_reference(self, node: NodeReference) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_sequence(self, node: NodeSequence) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_or(self, node: NodeOr) -> T:
        raise NotImplementedError()

    def visit(self, node: Node) -> T:
        if isinstance(node, NodeLiteral):
            return self.visit_literal(node)
        elif isinstance(node, NodeReference):
            return self.visit_reference(node)
        elif isinstance(node, NodeSequence):
            return self.visit_sequence(node)
        elif isinstance(node, NodeOr):
            return self.visit_or(node)
        else:
            raise NotImplementedError(node)


class _VisitorIterable(_AbstractVisitor[Iterator[Node]]):
    """Iterate over all the nodes in prefix order."""

    def visit_literal(self, node: NodeLiteral) -> Iterator[Node]:
        yield node

    def visit_reference(self, node: NodeReference) -> Iterator[Node]:
        yield node

    def visit_sequence(self, node: NodeSequence) -> Iterator[Node]:
        yield node
        for reference in node.references:
            yield from self.visit(reference)

    def visit_or(self, node: NodeOr) -> Iterator[Node]:
        yield node
        for sequence in node.sequences:
            yield from self.visit(sequence)


def iterate(rule_tree: Node) -> Iterator[Node]:
    """Yield the ``rule_tree`` and all its descendants."""
    visitor = _VisitorIterable()
    yield from visitor.visit(rule_tree)


class _VisitorStr(_AbstractVisitor[str]):
    """Represent the abstract syntax tree as string for easier inspection."""

    def visit_literal(self, node: NodeLiteral) -> str:
        return f'Lit("{node.literal}")'

    def visit_reference(self, node: NodeReference) -> str:
        return f"Ref({node.identifier})"

    def visit_sequence(self, node: NodeSequence) -> str:
        parts = " ".join(self.visit(reference) for reference in node.references)
        return f"Seq({parts})"

    def visit_or(self, node: NodeOr) -> str:
        parts = " | ".join(self.visit(sequence) for sequence in node.sequences)
        return f"Or({parts})"


def repr_rule_tree(rule_tree: Node) -> str:
    """Represent the abstract syntax tree ``rule_tree`` as a string for inspection."""
    visitor = _VisitorStr()
    return visitor.visit(rule_tree)


@require(lambda rule_trees: 0 in rule_trees, "The initial rule is present.")
# fmt: off
@require(
    lambda rule_trees:
    all(
        all(
            node.identifier in rule_trees
            for node in iterate(rule_tree)
            if isinstance(node, NodeReference)
        )
        for rule_tree in rule_trees.values()
    ),
    "No dangling references"
)
# fmt: on
def interpret_rule_0(rule_trees: Mapping[int, Node]) -> Rule:
    """Interpret the rule trees and construct the rule 0."""
    # This serves as a cache so that an already interpreted tree is not re-interpreted.
    interpreted_rules = dict()  # type: MutableMapping[int, Rule]

    # fmt: off
    @ensure(
        lambda rule_tree, result:
        not (isinstance(rule_tree, NodeReference)) or (
                rule_tree.identifier in interpreted_rules
                and result == interpreted_rules[rule_tree.identifier]
        )
    )
    # fmt: on
    def interpret_rule_tree(rule_tree: Node) -> Rule:
        if isinstance(rule_tree, NodeReference):
            if rule_tree.identifier in interpreted_rules:
                return interpreted_rules[rule_tree.identifier]

            if rule_tree.identifier not in rule_trees:
                raise ValueError(
                    f"The reference to the rule is dangling: {rule_tree.identifier}"
                )

            rule = interpret_rule_tree(rule_tree=rule_trees[rule_tree.identifier])
            interpreted_rules[rule_tree.identifier] = rule
            return rule

        elif isinstance(rule_tree, NodeLiteral):
            return RuleLiteral(literal=rule_tree.literal)

        elif isinstance(rule_tree, NodeSequence):
            return RuleSequence(
                rules=[
                    interpret_rule_tree(rule_tree=reference)
                    for reference in rule_tree.references
                ]
            )

        elif isinstance(rule_tree, NodeOr):
            return RuleOr(
                rules=[
                    interpret_rule_tree(rule_tree=sequence)
                    for sequence in rule_tree.sequences
                ]
            )

        else:
            raise NotImplementedError(rule_tree)

    return interpret_rule_tree(rule_tree=rule_trees[0])


@ensure(lambda messages, result: 0 <= result <= len(messages))
def count_matching_messages(rule_0: Rule, messages: List[str]) -> int:
    """Count the ``messages`` that match the rules starting from ``rule_0``."""
    result = 0
    for message in messages:
        remaining_suffix = rule_0.match(message)
        if remaining_suffix is not None and len(remaining_suffix) == 0:
            result += 1

    return result
