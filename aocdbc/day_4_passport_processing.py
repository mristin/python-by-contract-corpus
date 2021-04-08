from re import fullmatch
import sys
from typing import Dict, List, Optional

from icontract import require, ensure

_REQUIRED_KEYS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


@ensure(lambda: True)
def blank_line_split(text: str) -> List[str]:
    # NOTE: I tried to do a lookahead for the 2nd newline, but split doesn't take
    # a regex.
    return text.split("\n\n")


@ensure(lambda: True)
def parse(passport: str) -> Optional[Dict[str, str]]:
    result = {}
    for tok in passport.split():
        pair = tok.split(":", 2)
        if len(pair) != 2:
            return None
        result[pair[0]] = pair[1]
    return result


@ensure(lambda entry, result: result == (not (_REQUIRED_KEYS - entry.keys())))
def is_valid(entry: Dict[str, str]) -> bool:
    return len(_REQUIRED_KEYS - entry.keys()) == 0


@ensure(lambda result: result >= 0)
def count_valid(batch: str) -> int:
    count = 0
    for passport_text in blank_line_split(batch):
        passport = parse(passport_text)
        if passport and is_valid(passport):
            count += 1
    return count


# part 2


@ensure(lambda: True)
def is_valid2(entry: Dict[str, str]) -> bool:
    if not is_valid(entry):
        return False
    for key, value in entry.items():
        if not is_kv_valid2(key, value):
            return False
    return True


@ensure(lambda: True)
def is_kv_valid2(key: str, value: str) -> object:
    if key == "byr":
        # four digits; at least 1920 and at most 2002.
        return fullmatch(r"\d{4}", value) and (1920 <= int(value) <= 2002)
    elif key == "iyr":
        # four digits; at least 2010 and at most 2020.
        return fullmatch(r"\d{4}", value) and (2010 <= int(value) <= 2020)
    elif key == "eyr":
        # four digits; at least 2020 and at most 2030.
        return fullmatch(r"\d{4}", value) and (2020 <= int(value) <= 2030)
    elif key == "hgt":
        # a number followed by either cm or in:
        #  If cm, the number must be at least 150 and at most 193.
        #  If in, the number must be at least 59 and at most 76.
        if fullmatch(r".*cm", value):
            num = value[:-2]
            return fullmatch(r"\d+", num) and (150 <= int(num) <= 193)
        elif fullmatch(r".*in", value):
            num = value[:-2]
            return fullmatch(r"\d+", num) and (59 <= int(num) <= 76)
        else:
            return False
    elif key == "hcl":
        return fullmatch(r"#(\d|[a-f]){6}", value)
        # a "#" followed by exactly six characters 0-9 or a-f.
    elif key == "ecl":
        # exactly one of: amb blu brn gry grn hzl oth.
        return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    elif key == "pid":
        # a nine-digit number, including leading zeroes.
        return fullmatch(r"[0-9]{9}", value)
    return True


@ensure(lambda result: result >= 0)
def count_valid2(batch: str) -> int:
    count = 0
    for passport_text in blank_line_split(batch):
        passport = parse(passport_text)
        if not passport:
            raise Exception
        if passport:
            if is_valid2(passport):
                count += 1
    return count


if __name__ == "__main__":
    data = "".join(sys.stdin.readlines())
    print("part 1", count_valid(data))
    print("part 2", count_valid2(data))
