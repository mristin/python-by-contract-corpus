import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_11_seating_system


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [day_11_seating_system.list_neighbourhood]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_apply_on_case(self) -> None:
        steps = [
            textwrap.dedent(
                """\
                L.LL.LL.LL
                LLLLLLL.LL
                L.L.L..L..
                LLLL.LL.LL
                L.LL.LL.LL
                L.LLLLL.LL
                ..L.L.....
                LLLLLLLLLL
                L.LLLLLL.L
                L.LLLLL.LL"""
            ),
            textwrap.dedent(
                """\
                #.##.##.##
                #######.##
                #.#.#..#..
                ####.##.##
                #.##.##.##
                #.#####.##
                ..#.#.....
                ##########
                #.######.#
                #.#####.##"""
            ),
            textwrap.dedent(
                """\
                #.LL.L#.##
                #LLLLLL.L#
                L.L.L..L..
                #LLL.LL.L#
                #.LL.LL.LL
                #.LLLL#.##
                ..L.L.....
                #LLLLLLLL#
                #.LLLLLL.L
                #.#LLLL.##"""
            ),
            textwrap.dedent(
                """\
                #.##.L#.##
                #L###LL.L#
                L.#.#..#..
                #L##.##.L#
                #.##.LL.LL
                #.###L#.##
                ..#.#.....
                #L######L#
                #.LL###L.L
                #.#L###.##"""
            ),
            textwrap.dedent(
                """\
                #.#L.L#.##
                #LLL#LL.L#
                L.L.L..#..
                #LLL.##.L#
                #.LL.LL.LL
                #.LL#L#.##
                ..L.L.....
                #L#LLLL#L#
                #.LLLLLL.L
                #.#L#L#.##"""
            ),
            textwrap.dedent(
                """\
                #.#L.L#.##
                #LLL#LL.L#
                L.#.L..#..
                #L##.##.L#
                #.#L.LL.LL
                #.#L#L#.##
                ..L.L.....
                #L#L##L#L#
                #.LLLLLL.L
                #.#L#L#.##"""
            ),
        ]

        layout = day_11_seating_system.parse_layout(lines=steps[0].splitlines())
        for i, step in enumerate(steps[1:]):
            layout, change_count = day_11_seating_system.apply(layout=layout)
            self.assertEqual(step, day_11_seating_system.repr_layout(layout=layout))

        # No change expected after the last step.
        layout, change_count = day_11_seating_system.apply(layout=layout)
        self.assertEqual(steps[-1], day_11_seating_system.repr_layout(layout=layout))
        self.assertEqual(0, change_count)

        occupied_count = day_11_seating_system.count_occupied(layout=layout)
        self.assertEqual(37, occupied_count)


if __name__ == "__main__":
    unittest.main()
