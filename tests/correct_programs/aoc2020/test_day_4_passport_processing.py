import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_4_passport_processing


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_4_passport_processing.is_valid,
            # NOTE: the preconditions for this one are too challenging to meet right now
            # day_4_passport_processing.count_valid
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_count_valid(self) -> None:
        sample_batch = textwrap.dedent(
            """\
            ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
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
        )

        self.assertEqual(2, day_4_passport_processing.count_valid(sample_batch))


if __name__ == "__main__":
    unittest.main()
