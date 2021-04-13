import unittest

import icontract_hypothesis

from aocdbc.day_18_operation_order import parse, Computation, compute


# class TestWithIcontractHypothesis(unittest.TestCase):
# TODO how to test this function? 'Computation' has no strategy
#     def test_compute(self) -> None:
#         icontract_hypothesis.test_with_inferred_strategy(compute)
#
#     def test_parse(self) -> None:
#         icontract_hypothesis.test_with_inferred_strategy(parse)


computation_test_objects = [  # "1 + 2 * 3 + 4 * 5 + 6"
                           Computation(operators=['+', '*', '+', '*', '+'],
                                       operands=[1, 2, 3, 4, 5, 6]),
                           # "1 + (2 * 3) + (4 * (5 + 6))"
                           Computation(operators=['+', '+'],
                                       operands=[
                                           1,
                                           Computation(operators=['*'],
                                                       operands=[2, 3]),
                                           Computation(operators=['*'],
                                                       operands=[
                                                           4,
                                                           Computation(
                                                               operators=['+'],
                                                               operands=[5, 6])])]),
                           # "2 * 3 + (4 * 5)"
                           Computation(operators=['*', '+'],
                                       operands=[2, 3, Computation(operators=['*'],
                                                                   operands=[4, 5])]),
                           # "5 + (8 * 3 + 9 + 3 * 4 * 3)"
                           Computation(operators=['+'],
                                       operands=[
                                           5,
                                           Computation(
                                               operators=['*', '+', '+', '*', '*'],
                                               operands=[8, 3, 9, 3, 4, 3])]),
                           # "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
                           Computation(operators=['*', '*'],
                                       operands=[5,
                                                 9,
                                                 Computation(
                                                     operators=['*', '*', '+',
                                                                '*', '+'],
                                                     operands=[7, 3, 3, 9, 3,
                                                               Computation(
                                                                   operators=['+', '*'],
                                                                   operands=[8, 6, 4])])
                                                 ]),
                           # "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
                           Computation(operators=['+', '+', '*'],
                                       operands=[
                                           Computation(
                                               operators=['*', '+'],
                                               operands=[
                                                   Computation(
                                                       operators=['+', '*'],
                                                       operands=[2, 4, 9]),
                                                   Computation(
                                                       operators=['+', '*', '+'],
                                                       operands=[6, 9, 8, 6]),
                                                   6]),
                                           2, 4, 2])]


class TestManuallyParse(unittest.TestCase):
    def test_case(self) -> None:
        test_input = ["1 + 2 * 3 + 4 * 5 + 6",
                      "1 + (2 * 3) + (4 * (5 + 6))",
                      "2 * 3 + (4 * 5)",
                      "5 + (8 * 3 + 9 + 3 * 4 * 3)",
                      "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
                      "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]

        expected_output = computation_test_objects
        for test_pair in zip(test_input, expected_output):
            self.assertEqual(test_pair[1], parse(test_pair[0]))


class TestManuallyCompute(unittest.TestCase):
    def test_case(self) -> None:
        test_input = computation_test_objects
        expected_output = [71,
                           51,
                           26,
                           437,
                           12240,
                           13632]
        for test_pair in zip(test_input, expected_output):
            self.assertEqual(test_pair[0].compute(), test_pair[1])


if __name__ == "__main__":
    unittest.main()
