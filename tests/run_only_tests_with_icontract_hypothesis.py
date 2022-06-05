"""Run only icontract-hypothesis tests matching ``TestWithIcontractHypothesis``."""

import importlib
import os
import pathlib
import sys
import unittest


def main() -> int:
    """Execute the main routine."""
    this_path = pathlib.Path(os.path.realpath(__file__))
    tests_dir = this_path.parent

    test_suite = unittest.TestSuite()

    correct_dir = tests_dir / "correct"
    for pth in sorted(correct_dir.glob("**/test_*.py")):
        parts = ["tests"]
        parts.extend(pth.parent.relative_to(tests_dir).parts)
        parts.append(pth.stem)
        module_name = ".".join(parts)

        test_module = importlib.import_module(module_name)
        icontract_hypothesis_test_case = getattr(
            test_module, "TestWithIcontractHypothesis", None
        )

        if icontract_hypothesis_test_case is None:
            print(f"No icontract-hypothesis test case found in: {module_name}")
            continue

        test_method = getattr(icontract_hypothesis_test_case, "test_functions", None)
        if test_method is None:
            print(
                f"No test_functions found in {icontract_hypothesis_test_case.__name__} "
                f"of {module_name}"
            )
            continue

        test_suite.addTest(icontract_hypothesis_test_case("test_functions"))

    print("Executing the tests...")
    unittest.TextTestRunner(verbosity=3).run(test_suite)

    return 0


if __name__ == "__main__":
    sys.exit(main())
