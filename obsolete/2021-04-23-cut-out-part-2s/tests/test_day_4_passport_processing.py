import unittest

import icontract_hypothesis

from correct_programs.aoc2020.day_4_passport_processing import (
    count_valid,
    is_valid,
)

_SAMPLE_BATCH = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""


class TestDay4(unittest.TestCase):
    def test_part1(self) -> None:
        self.assertEqual(count_valid(_SAMPLE_BATCH), 2)

    def test_is_valid_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(is_valid)

#     NOTE: the preconditions for this one are too challenging to meet right now:
#     def test_count_valid_with_icontract_hypothesis(self) -> None:
#         icontract_hypothesis.test_with_inferred_strategy(count_valid)


if __name__ == "__main__":
    unittest.main()
