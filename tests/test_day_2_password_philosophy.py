import unittest

import icontract_hypothesis

import aocdbc.day_2_password_philosophy


class TestDay2(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ("1-3 a: abcde", True),
            ("1-3 b: cdefg", False),
            ("2-9 c: ccccccccc", True),
        ]

        for line, expected_result in cases:
            result = aocdbc.day_2_password_philosophy.verify_line(line=line)
            self.assertEqual(expected_result, result)

    def test_verify_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_2_password_philosophy.verify
        )

    def test_verify_line_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_2_password_philosophy.verify_line
        )


if __name__ == "__main__":
    unittest.main()
