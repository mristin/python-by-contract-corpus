from icontract import ensure, require
import regex as re


@require(lambda input_string: all(re.match(r'^[a-z]*$', line) for line in input_string.split('\n')))
@require(lambda input_string: all(len(set(list(line))) == len(line) for line in input_string.split('\n')))
@ensure(lambda result: result >= 0)
def solve(input_string: str) -> int:
    count = 0
    yes_answers = set()
    for line in input_string.split('\n'):
        if line:
            yes_answers = yes_answers.union(list(line))
        else:
            count += len(yes_answers)
            yes_answers.clear()
    count += len(yes_answers)
    return count
