from typing import Tuple, List
from icontract import ensure, require
import re

"""
icontract.errors.ViolationError: File /home/lauren/Nextcloud/Documents/2020-2021/thesis/code/aocdbc/aocdbc/day_3_toboggan_trajectory.py, line 11 in <module>:
all(len(line) == len(input_string.split('\n')[0]) for line in input_string.split('\n')):
all(len(line) == len(input_string.split('\n')[0]) for line in input_string.split('\n')) was False
input_string was '..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#\n'
input_string.split('\n') was ['..##.......', '#...#...#..', '.#....#..#.', '..#.#...#.#', '.#...##..#.', '..#.##.....', '.#.#.#....#', '.#........#', '#.##...#...', '#...##....#', '.#..#...#.#', '']
"""

step_size_horizontal: int = 3
step_size_vertical: int = 1


@require(lambda input_string: re.match(r'^([.#]*\\n)+$', input_string),)
@require(lambda input_string: all(len(line) == len(input_string.split('\n')[0]) for line in input_string.split('\n')))
@ensure(lambda result: result[0] * result[1] == len(result[2]))
def parse_input_file(input_string: str) -> Tuple[int, int, str]:
    lines = input_string.split('\n')
    width: int = len(lines[0])
    height: int = len(lines)
    return width, height, "".join(lines)


@require(lambda width, height: width > 0 and height > 0)
@require(lambda input_string: re.match(r'^[.#]*', input_string))
@require(lambda width, height, input_string: width * height == len(input_string))
@ensure(lambda result, height: result <= height / step_size_vertical)
def count_trees(width: int, height: int, input_string: str):
    count: int = 0
    current_x: int = 0
    current_y: int = 0

    while current_y < height:
        if input_string[current_y * width + current_x] == "#":
            count += 1
        current_x = (current_x + step_size_horizontal) % width
        current_y += step_size_vertical

    return count