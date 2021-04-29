import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_17_conway_cubes


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_17_conway_cubes.are_neighbours,
            day_17_conway_cubes.list_neighbourhood,
            day_17_conway_cubes.apply,
            day_17_conway_cubes.count_active,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        lines = textwrap.dedent(
            """\
            .#.
            ..#
            ###"""
        ).splitlines()

        activity = day_17_conway_cubes.parse_initial(lines=lines)

        expected_reprs = [
            textwrap.dedent(
                """\
                z=0
                .#.
                ..#
                ###"""
            ),
            textwrap.dedent(
                """\
                z=-1
                #..
                ..#
                .#.
                
                z=0
                #.#
                .##
                .#.
                
                z=1
                #..
                ..#
                .#."""
            ),
            textwrap.dedent(
                """\
                z=-2
                .....
                .....
                ..#..
                .....
                .....
                
                z=-1
                ..#..
                .#..#
                ....#
                .#...
                .....
                
                z=0
                ##...
                ##...
                #....
                ....#
                .###.
                
                z=1
                ..#..
                .#..#
                ....#
                .#...
                .....
                
                z=2
                .....
                .....
                ..#..
                .....
                ....."""
            ),
            textwrap.dedent(
                """\
            z=-2
            .......
            .......
            ..##...
            ..###..
            .......
            .......
            .......
            
            z=-1
            ..#....
            ...#...
            #......
            .....##
            .#...#.
            ..#.#..
            ...#...
            
            z=0
            ...#...
            .......
            #......
            .......
            .....##
            .##.#..
            ...#...
            
            z=1
            ..#....
            ...#...
            #......
            .....##
            .#...#.
            ..#.#..
            ...#...
            
            z=2
            .......
            .......
            ..##...
            ..###..
            .......
            .......
            ......."""
            ),
        ]

        self.assertEqual(
            expected_reprs[0],
            day_17_conway_cubes.repr_activity(activity=activity),
        )

        cycle = 1
        for expected_repr in expected_reprs[1:]:
            activity = day_17_conway_cubes.apply(activity=activity)

            self.assertEqual(
                expected_repr,
                day_17_conway_cubes.repr_activity(activity=activity),
                f"after {cycle} cycle",
            )

            cycle += 1

        # Simulate for 3 more cycles
        for _ in range(3):
            activity = day_17_conway_cubes.apply(activity=activity)

        self.assertEqual(112, day_17_conway_cubes.count_active(activity=activity))


if __name__ == "__main__":
    unittest.main()
