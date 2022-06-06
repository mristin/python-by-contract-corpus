"""Compute the statistics about the contracts in the corpus."""

import argparse
import ast
import collections
import enum
import importlib
import inspect
import os
import pathlib
import re
import sys
from typing import MutableMapping, Callable, Any, Optional

import icontract
import icontract._represent
import regex


class ConditionCategory(enum.Enum):
    BOUND = "bound"
    PATTERN = "pattern"
    ALL_QUANTIFIER = "all_quantifier"
    OTHER = "other"


def _categorize_condition(condition: Callable[..., Any]) -> ConditionCategory:
    """Categorize the condition of a contract."""
    if not icontract._represent.is_lambda(a_function=condition):
        return ConditionCategory.OTHER

    lines, condition_lineno = inspect.findsource(condition)
    filename = inspect.getsourcefile(condition)
    assert filename is not None

    decorator_inspection = icontract._represent.inspect_decorator(
        lines=lines, lineno=condition_lineno, filename=filename
    )
    lambda_inspection = icontract._represent.find_lambda_condition(
        decorator_inspection=decorator_inspection
    )

    assert (
        lambda_inspection is not None
    ), "Expected lambda_inspection to be non-None if _is_lambda is True on: {}".format(
        condition
    )

    body_node = lambda_inspection.node.body

    if isinstance(body_node, ast.Compare):
        if (
            isinstance(body_node.left, ast.Constant)
            and len(body_node.comparators) == 1
            and isinstance(body_node.comparators[0], ast.Name)
        ) or (
            isinstance(body_node.left, ast.Name)
            and len(body_node.comparators) == 1
            and isinstance(body_node.comparators[0], ast.Constant)
        ):
            return ConditionCategory.BOUND
        else:
            return ConditionCategory.OTHER
    elif (
        isinstance(body_node, ast.Call)
        and isinstance(body_node.func, ast.Name)
        and body_node.func.id == "all"
    ):
        return ConditionCategory.ALL_QUANTIFIER
    elif (
        isinstance(body_node, ast.Call)
        and isinstance(body_node.func, ast.Attribute)
        and isinstance(body_node.func.value, ast.Name)
        and body_node.func.attr in ("fullmatch", "match")
    ):
        module_qualname = getattr(condition, "__module__", None)
        assert (
            module_qualname is not None
        ), f"Expected __module__ in condition {condition}"

        module = sys.modules[module_qualname]

        obj = getattr(module, body_node.func.value.id, None)
        assert (
            obj is not None
        ), f"Unexpected missing attribute {body_node.func.value.id} in {module=}"

        if obj == re or obj == regex or isinstance(obj, re.Pattern):
            return ConditionCategory.PATTERN
        else:
            return ConditionCategory.OTHER
    else:
        # TODO (mristin, 2022-06-6): match against more categories?
        return ConditionCategory.OTHER


def main() -> int:
    """Execute the main routine."""
    repo_root = pathlib.Path(os.path.realpath(__file__)).parent.parent

    invariants_histo = collections.defaultdict(
        lambda: 0
    )  # type: MutableMapping[int, int]
    preconditions_histo = collections.defaultdict(
        lambda: 0
    )  # type: MutableMapping[int, int]
    postconditions_histo = collections.defaultdict(
        lambda: 0
    )  # type: MutableMapping[int, int]

    preconditions_categories_histo = collections.defaultdict(
        lambda: 0
    )  # type: MutableMapping[ConditionCategory, int]

    def consider_function(function_point: Callable[..., Any]) -> None:
        """
        Include the ``function_point`` in the statistics.

        The ``function_point`` can be a function or a method of a class.
        """
        preconditions = getattr(function_point, "__preconditions__", None)
        if preconditions is not None:
            # NOTE (mristin, 2022-06-06):
            # Pre-conditions are given as a disjunction of conjunctions.
            # We simply sum them all up here.
            precondition_count = sum(len(conjunction) for conjunction in preconditions)
        else:
            precondition_count = 0

        preconditions_histo[precondition_count] += 1

        # region Categorize the pre-conditions

        if preconditions is not None:
            for conjunction in preconditions:
                for contract in conjunction:
                    category = _categorize_condition(condition=contract.condition)

                    preconditions_categories_histo[category] += 1

        # endregion

        postconditions = getattr(function_point, "__postconditions__", None)
        if postconditions is not None:
            postcondition_count = len(postconditions)
        else:
            postcondition_count = 0

        postconditions_histo[postcondition_count] += 1

    for pth in sorted(
        (repo_root / "python_by_contract_corpus" / "correct").glob("**/*.py")
    ):
        module_name = ".".join(
            list(pth.parent.relative_to(repo_root).parts) + [pth.stem]
        )
        module = importlib.import_module(module_name)

        for attr in dir(module):
            if attr.startswith("__"):
                continue

            item = getattr(module, attr)
            item_module = getattr(item, "__module__", None)
            if item_module is None:
                continue

            if item_module != module.__name__:
                continue

            if inspect.isfunction(item):
                consider_function(function_point=item)
            elif inspect.isclass(item):
                invariants = getattr(item, "__invariants__", None)
                if invariants is not None:
                    invariant_count = len(invariants)
                else:
                    invariant_count = 0
                invariants_histo[invariant_count] += 1

                for class_attr in vars(item):
                    class_item = getattr(item, class_attr)

                    if inspect.isfunction(class_item):
                        consider_function(function_point=class_item)
                    else:
                        # NOTE (mristin, 2022-06-06):
                        # We simply ignore the rest as implementation of the closed-set
                        # would be too difficult.
                        pass

            else:
                # NOTE (mristin, 2022-06-06):
                # We simply ignore the rest as implementation of the closed-set
                # would be too difficult.
                pass

    print("Precondition stats (# of preconditions / # of function points):")
    total = 0
    total_preconditions = 0

    key = None  # type: Optional[Any]

    for key in sorted(preconditions_histo.keys()):
        print(f"  {key:3d}: {preconditions_histo[key]:3d}")
        total += preconditions_histo[key]
        total_preconditions += key * preconditions_histo[key]
    print(f"  Total function points: {total}")
    print(f"  Total preconditions: {total_preconditions}")

    print()
    print("Categories of preconditions (category / # of preconditions):")
    total_preconditions = 0
    for _, key in sorted(
        (key.value, key) for key in preconditions_categories_histo.keys()
    ):
        print(f"  {key.value:15s}: {preconditions_categories_histo[key]:3d}")
        total_preconditions += preconditions_categories_histo[key]
    print(f"  Total preconditions: {total_preconditions}")

    print()
    print("Post-condition stats (# of post-conditions / # of function points):")
    total = 0
    total_postconditions = 0
    for key in sorted(postconditions_histo.keys()):
        print(f"  {key:3d}: {postconditions_histo[key]:3d}")
        total += postconditions_histo[key]
        total_postconditions += key * postconditions_histo[key]
    print(f"  Total: {total}")
    print(f"  Total post-conditions: {total_postconditions}")

    print()
    print("Invariants (# of classes / # of invariants):")
    total = 0
    for key in sorted(invariants_histo.keys()):
        print(f"  {key:3d}: {invariants_histo[key]:3d}")
        total += invariants_histo[key]
    print(f"  Total: {total}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
