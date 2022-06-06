import unittest

import icontract_hypothesis

from python_by_contract_corpus.correct.aoc2020 import day_18_operation_order


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [day_18_operation_order.serialize, day_18_operation_order.compute]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    test_expressions = ["(1+2)+(3*4)", "(1+(2*3))+4", "1+2*3+4+6*7"]  # 15  # 11  # 133

    test_nodes = [
        day_18_operation_order.Node(
            head=day_18_operation_order.Node(
                head=1,
                tail=[
                    day_18_operation_order.Tail(
                        op=day_18_operation_order.Operation.ADD, right=2
                    )
                ],
            ),
            tail=[
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.ADD,
                    right=day_18_operation_order.Node(
                        head=3,
                        tail=[
                            day_18_operation_order.Tail(
                                op=day_18_operation_order.Operation.MUL, right=4
                            )
                        ],
                    ),
                )
            ],
        ),
        day_18_operation_order.Node(
            head=day_18_operation_order.Node(
                head=1,
                tail=[
                    day_18_operation_order.Tail(
                        op=day_18_operation_order.Operation.ADD,
                        right=day_18_operation_order.Node(
                            head=2,
                            tail=[
                                day_18_operation_order.Tail(
                                    op=day_18_operation_order.Operation.MUL, right=3
                                )
                            ],
                        ),
                    )
                ],
            ),
            tail=[
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.ADD, right=4
                )
            ],
        ),
        day_18_operation_order.Node(
            head=1,
            tail=[
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.ADD, right=2
                ),
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.MUL, right=3
                ),
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.ADD, right=4
                ),
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.ADD, right=6
                ),
                day_18_operation_order.Tail(
                    op=day_18_operation_order.Operation.MUL, right=7
                ),
            ],
        ),
    ]

    test_results = [15, 11, 133]

    def test_parse(self) -> None:
        for expr, node in zip(self.test_expressions, self.test_nodes):
            self.assertEqual(node, day_18_operation_order.parse(expr))

    def test_serialize(self) -> None:
        for expr, node in zip(self.test_expressions, self.test_nodes):
            self.assertEqual(expr, day_18_operation_order.serialize(node))

    def test_compute(self) -> None:
        for node, result in zip(self.test_nodes, self.test_results):
            self.assertEqual(result, day_18_operation_order.compute(node))


if __name__ == "__main__":
    unittest.main()
