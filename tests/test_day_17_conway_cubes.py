import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_17_conway_cubes


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_are_neighbours(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_17_conway_cubes.are_neighbours
        )

    def test_list_neighbourhood(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_17_conway_cubes.list_neighbourhood
        )

    def test_apply(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_17_conway_cubes.apply
        )

    def test_count_active(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_17_conway_cubes.count_active
        )


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        lines = textwrap.dedent(
            """\
            .#.
            ..#
            ###"""
        ).splitlines()

        activity = aocdbc.day_17_conway_cubes.parse_initial(lines=lines)

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
            aocdbc.day_17_conway_cubes.repr_activity(activity=activity),
        )

        cycle = 1
        for expected_repr in expected_reprs[1:]:
            activity = aocdbc.day_17_conway_cubes.apply(activity=activity)

            self.assertEqual(
                expected_repr,
                aocdbc.day_17_conway_cubes.repr_activity(activity=activity),
                f"after {cycle } cycle",
            )

            cycle += 1

        # Simulate for 3 more cycles
        for _ in range(3):
            activity = aocdbc.day_17_conway_cubes.apply(activity=activity)

        self.assertEqual(
            112, aocdbc.day_17_conway_cubes.count_active(activity=activity)
        )


if __name__ == "__main__":
    unittest.main()
