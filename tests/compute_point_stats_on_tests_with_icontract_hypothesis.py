"""Compute statistics on coverage of the icontract-hypothesis."""
import ast
import importlib
import inspect
import os
import pathlib
import re
import sys
import unittest
from typing import Sequence, Optional, Set

import asttokens

_REPO_ROOT = pathlib.Path(os.path.realpath(__file__)).parent.parent
_TESTS_DIR = _REPO_ROOT / "tests"


def list_function_points() -> Set[str]:
    """
    List all the function points in the ``correct`` module

    A function point is either a function or a method.
    """
    point_set = set()  # type: Set[str]

    for pth in sorted(
        (_REPO_ROOT / "python_by_contract_corpus" / "correct").glob("**/*.py")
    ):
        module_name = ".".join(
            list(pth.parent.relative_to(_REPO_ROOT).parts) + [pth.stem]
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
                point = f"{module.__name__}.{item.__name__}"
                point_set.add(point)
            elif inspect.isclass(item):
                for class_attr in vars(item):
                    class_item = getattr(item, class_attr)

                    if inspect.isfunction(class_item):
                        point = (
                            f"{module.__name__}.{item.__name__}.{class_item.__name__}"
                        )
                        point_set.add(point)
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

    return point_set


def main() -> int:
    """Execute the main routine."""
    test_paths = sorted((_REPO_ROOT / "tests" / "correct").glob("**/test_*.py"))

    print("Computing the stats on the functions matched by icontract-hypothesis...")

    point_set = list_function_points()

    points_directly_covered = set()  # type: Set[str]
    points_requiring_set_up = set()  # type: Set[str]

    look_up_for_set_ups = {
        ("tests.correct.aoc2020.test_day_25_combo_breaker", "transform_testable"): (
            "python_by_contract_corpus.correct"
            ".aoc2020.day_25_combo_breaker.transform"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_02.test_problem_02",
            "draw_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_02.problem_02.draw"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_02.test_problem_05_01",
            "draw_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_02.problem_05_01.draw"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_03.test_problem_01",
            "compute_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_03.problem_01.compute"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_03.test_problem_02",
            "repr_binary_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_03.problem_02.repr_binary"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_03.test_problem_03",
            "gcd_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_03.problem_03.gcd"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_04.test_problem_01",
            "sieve_with_restricted_input",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_04.problem_01.sieve"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_08.test_problem_03",
            "restricted_simulate",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_08.problem_03.simulate"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_08.test_problem_05",
            "restricted_simulate",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_08.problem_05.simulate"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_11.test_problem_02",
            "smoke_test_evaluate_call",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_11.problem_02.evaluate"
        ),
        (
            "tests.correct.ethz_eprog_2019.exercise_11.test_problem_02",
            "smoke_test_evaluate_expr",
        ): (
            "python_by_contract_corpus.correct"
            ".ethz_eprog_2019.exercise_11.problem_02.evaluate"
        ),
    }

    for pth in test_paths:
        atok = asttokens.ASTTokens(
            source_text=pth.read_text(encoding="utf-8"), parse=True, filename=str(pth)
        )

        module_node = atok.tree
        assert isinstance(module_node, ast.Module)

        test_function_def = None  # type: Optional[ast.FunctionDef]
        for module_body_node in module_node.body:
            if (
                isinstance(module_body_node, ast.ClassDef)
                and module_body_node.name == "TestWithIcontractHypothesis"
            ):
                for class_body_node in module_body_node.body:
                    if (
                        isinstance(class_body_node, ast.FunctionDef)
                        and class_body_node.name == "test_functions"
                    ):
                        test_function_def = class_body_node
                        break

        if test_function_def is None:
            print(f"No test_functions found in TestWithIcontractHypothesis of {pth}")
            continue

        for_node = None  # type: Optional[ast.For]
        for body_node in test_function_def.body:
            if isinstance(body_node, ast.For):
                for_node = body_node
                break

        assert for_node is not None, (
            f"Unexpected form of test_functions in {pth}: no ``for`` could be found: "
            f"{atok.get_text(test_function_def)}"
        )

        assert isinstance(for_node.iter, ast.List), (
            f"Unexpected from of ``for`` in test_functions "
            f"in {pth}: {atok.get_text(for_node)}"
        )

        relative_pth = pth.relative_to(_TESTS_DIR)
        module_under_test_name = re.sub(r"^test_", "", relative_pth.stem)
        module_under_test_qualname = ".".join(
            ["python_by_contract_corpus"]
            + list(relative_pth.parent.parts)
            + [module_under_test_name]
        )

        test_module_name = ".".join(
            list(pth.parent.relative_to(_REPO_ROOT).parts) + [pth.stem]
        )

        for elt_node in for_node.iter.elts:
            if isinstance(elt_node, ast.Name):
                key_tuple = (test_module_name, elt_node.id)

                point = look_up_for_set_ups.get(key_tuple, None)
                if point is None:
                    raise NotImplementedError(
                        f"We do not know how to count the element "
                        f"in the test_functions of {pth}: {key_tuple}"
                    )

                assert point in point_set, f"{point=}, {sorted(point_set)=}"
                points_requiring_set_up.add(point)

            elif isinstance(elt_node, ast.Attribute):
                if isinstance(elt_node.value, ast.Name):
                    assert (
                        elt_node.value.id == module_under_test_name
                    ), f"{elt_node.value.id=}, {module_under_test_name=}"

                    point = f"{module_under_test_qualname}.{elt_node.attr}"

                    assert point in point_set, f"{point=}, {sorted(point_set)=}"

                    points_directly_covered.add(point)
                elif isinstance(elt_node.value, ast.Attribute) and isinstance(
                    elt_node.value.value, ast.Name
                ):
                    assert (
                        elt_node.value.value.id == module_under_test_name
                    ), f"{elt_node.value.value.id=}, {module_under_test_name=}"

                    point = (
                        f"{module_under_test_qualname}"
                        f".{elt_node.value.attr}"
                        f".{elt_node.attr}"
                    )

                    assert point in point_set, f"{point=}, {sorted(point_set)=}"

                    points_directly_covered.add(point)

                else:
                    raise NotImplementedError(
                        f"Unexpected item in ``for`` of test_functions "
                        f"in {pth}: {ast.dump(elt_node)=}"
                    )
            else:
                raise NotImplementedError(
                    f"Unexpected item in ``for`` of test_functions "
                    f"in {pth}: {ast.dump(elt_node)=}"
                )

    print(f"Total number of function points: {len(point_set)}")
    print(
        f"Number of function points directly covered "
        f"by icontract-hypothesis: {len(points_directly_covered)}"
    )
    print(
        f"Number of function points covered by icontract-hypothesis "
        f"with a set-up wrapper: {len(points_requiring_set_up)}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
