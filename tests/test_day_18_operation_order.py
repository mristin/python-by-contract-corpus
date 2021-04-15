import unittest

import icontract_hypothesis

from aocdbc.day_18_operation_order import serialize, compute, Node, Operation, Tail, parse


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_serialize(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            serialize
        )

    def test_compute(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            compute
        )


class ManualTests(unittest.TestCase):
    test_expressions = ['(1+2)+(3*4)',  # 15
                        '(1+(2*3))+4',  # 11
                        '1+2*3+4+6*7']  # 133

    test_nodes = [
        Node(head=Node(head=1, tail=[Tail(op=Operation.ADD, right=2)]), tail=[Tail(op=Operation.ADD, right=Node(head=3, tail=[Tail(op=Operation.MUL, right=4)]))]),
        Node(head=Node(head=1, tail=[Tail(op=Operation.ADD, right=Node(head=2, tail=[Tail(op=Operation.MUL, right=3)]))]), tail=[Tail(op=Operation.ADD, right=4)]),
        Node(head=1, tail=[Tail(op=Operation.ADD, right=2), Tail(op=Operation.MUL, right=3), Tail(op=Operation.ADD, right=4), Tail(op=Operation.ADD, right=6), Tail(op=Operation.MUL, right=7)])
    ]

    test_results = [15, 11, 133]

    def test_parse(self) -> None:
        for expr, node in zip(self.test_expressions, self.test_nodes):
            self.assertEqual(node, parse(expr))

    def test_serialize(self) -> None:
        for expr, node in zip(self.test_expressions, self.test_nodes):
            self.assertEqual(expr, serialize(node))

    def test_compute(self) -> None:
        for node, result in zip(self.test_nodes, self.test_results):
            self.assertEqual(result, compute(node))


if __name__ == "__main__":
    unittest.main()
