import random
import unittest

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_06 import problem_04


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_methods(self) -> None:
        for func in [
            problem_04.LinkedList.add_first,
            problem_04.LinkedList.add_last,
            problem_04.LinkedList.count,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error

    def test_with_state(self) -> None:
        lst = problem_04.LinkedList()

        all_methods_set = {
            lst.add_first,
            lst.count,
            lst.remove_first,
            lst.remove_last,
            lst.clear,
            lst.is_empty,
            lst.get,
            lst.set,
        }

        all_methods = tuple(all_methods_set)

        # NOTE (mristin, 2021-05-16):
        # Unfortunately, icontract-hypothesis is at the moment not intelligent
        # enough to figure out which methods can be automatically executed.
        # This should change in the future.
        methods_if_empty = tuple(
            all_methods_set.difference(
                {lst.remove_first, lst.remove_last, lst.clear, lst.get, lst.set}
            )
        )

        for _ in range(100):
            methods = all_methods
            if lst.is_empty():
                methods = methods_if_empty

            method = random.choice(methods)

            try:
                icontract_hypothesis.test_with_inferred_strategy(method)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {method} with icontract-hypothesis "
                    f"failed (please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()
