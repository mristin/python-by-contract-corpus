import regex
from typing import List, Dict, Set, Final

from icontract import require, ensure, DBC


class Ingredient:
    identifier: Final[str]

    @require(lambda identifier: regex.match("^[a-zA-Z]+$", identifier))
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


class Allergen(DBC):
    identifier: Final[str]

    @require(lambda identifier: regex.match("^[a-zA-Z]+$", identifier))
    def __init__(self, identifier: str) -> None:
        self.identifier: str = identifier
        self.potential_ingredients: List[Set[Ingredient]] = []

    def __repr__(self) -> str:
        return "{}, {}".format(self.identifier, self.potential_ingredients)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Allergen):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.potential_ingredients == other.potential_ingredients
        )

    def add_potential_ingredients_set(
        self, potential_ingredients: Set[Ingredient]
    ) -> None:
        self.potential_ingredients.append(set(potential_ingredients))

    def intersection_potential_ingredients(self) -> Set[Ingredient]:
        return set.intersection(*self.potential_ingredients)


# small error: this allows for "ing1 ing2 (contains , soy, water)"
ALLERGEN_LINE_RE = regex.compile(
    r"^(?:\s?(?P<ingredient>\w+))* " r"\(contains (?:(?:,\s)?(?P<allergen>\w+))*\)$"
)


@require(lambda line_1: ALLERGEN_LINE_RE.match(line_1))
@require(lambda line_2: ALLERGEN_LINE_RE.match(line_2))
def is_equal_ingredient_line(line_1: str, line_2: str) -> bool:
    mtch1 = ALLERGEN_LINE_RE.match(line_1)
    assert mtch1 is not None

    ingredients_in_line_1 = set(mtch1.captures(1))
    allergens_in_line_1 = set(mtch1.captures(2))

    mtch2 = ALLERGEN_LINE_RE.match(line_2)
    assert mtch2 is not None

    ingredients_in_line_2 = set(mtch2.captures(1))
    allergens_in_line_2 = set(mtch2.captures(2))

    return (
        ingredients_in_line_1 == ingredients_in_line_2
        and allergens_in_line_1 == allergens_in_line_2
    )


@require(
    lambda ingredient_list_1: all(
        ALLERGEN_LINE_RE.match(line) for line in ingredient_list_1
    )
)
@require(
    lambda ingredient_list_2: all(
        ALLERGEN_LINE_RE.match(line) for line in ingredient_list_2
    )
)
def is_equal_ingredient_list(
    ingredient_list_1: List[str], ingredient_list_2: List[str]
) -> bool:
    if len(ingredient_list_1) != len(ingredient_list_2):
        return False
    for l1 in ingredient_list_1:
        if not any(is_equal_ingredient_line(l1, l2) for l2 in ingredient_list_2):
            return False
    for l2 in ingredient_list_2:
        if not any(is_equal_ingredient_line(l2, l1) for l1 in ingredient_list_1):
            return False
    return True


# fmt: off
@require(lambda lines: all(ALLERGEN_LINE_RE.match(line) for line in lines))
@ensure(
    lambda result, lines:
    is_equal_ingredient_list(serialize(result), lines)  # type: ignore
)
# fmt: on
def parse_list_of_foods(lines: List[str]) -> List[Allergen]:
    allergens: Dict[str, Allergen] = dict()
    for line in lines:
        ingredients_in_line = ALLERGEN_LINE_RE.match(line).captures(1)
        allergens_in_line = ALLERGEN_LINE_RE.match(line).captures(2)
        for allergen in allergens_in_line:
            if allergen not in allergens:
                allergens[allergen] = Allergen(allergen)
            allergens[allergen].add_potential_ingredients_set(ingredients_in_line)
    return list(allergens.values())


@require(
    lambda allergen_set: all(
        len(allergen.potential_ingredients) > 0 for allergen in allergen_set
    )
)
@ensure(lambda result, allergen_set: allergen_set == parse_list_of_foods(result))
def serialize(allergen_set: List[Allergen]) -> List[str]:
    ingredient_groups: Dict[str, List[Allergen]] = dict()
    for allergen in allergen_set:
        for ingredient_set in allergen.potential_ingredients:
            ingredient_set_str = " ".join(
                [str(ingredient) for ingredient in ingredient_set]
            )
            if str(ingredient_set_str) in ingredient_groups.keys():
                ingredient_groups[str(ingredient_set_str)].append(allergen)
            else:
                ingredient_groups[str(ingredient_set_str)] = [allergen]
    ingredient_list: List[str] = []
    for ingredients, allergens in ingredient_groups.items():
        allergens_str: str = ", ".join(
            [str(allergen.identifier) for allergen in allergens]
        )
        ingredient_list.append("{} (contains {})".format(ingredients, allergens_str))
    return ingredient_list


ALLERGEN_LIST_RE = regex.compile(
    r"^(\s?\w+)* \(contains ((,\s)?\w+)*\)" r"(\n(\s?\w+)* \(contains ((,\s)?\w+)*\))*$"
)


@require(lambda puzzle_input: ALLERGEN_LIST_RE.match(puzzle_input))
def solve(puzzle_input: str) -> Set[Ingredient]:
    ingredient_lines = puzzle_input.split("\n")
    allergen_set = parse_list_of_foods(ingredient_lines)
    excluded_ingredients = set.union(
        *map(
            lambda allergen: allergen.intersection_potential_ingredients(), allergen_set
        )
    )
    all_ingredients = set.union(
        *map(lambda allergen: set.union(*allergen.potential_ingredients), allergen_set)
    )
    return all_ingredients.difference(excluded_ingredients)
