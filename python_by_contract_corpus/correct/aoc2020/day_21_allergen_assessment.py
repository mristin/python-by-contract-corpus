import re
from typing import List, Set, cast, MutableMapping

from icontract import require, ensure, DBC


class Identifier(DBC, str):
    """Represent an ingredient or allergen identifier."""

    @require(lambda value: re.fullmatch(r"^[a-zA-Z]+\Z", value))
    def __new__(cls, value: str) -> "Identifier":
        """Enforce the properties on the ``identifier``."""
        return cast(Identifier, value)


class Allergen(Identifier):
    """Represent an identifier of an allergen."""


class Ingredient(Identifier):
    """Represent an identifier of an ingredient."""


#: Express a line specifying an ingredient list along with the allergens.
INGREDIENT_LINE_RE = re.compile(
    r"\s*(?P<ingredients>[a-zA-Z]+(\s+[a-zA-Z]+)*)\s+"
    r"\(contains\s+(?P<allergens>[a-zA-Z]+(\s*,\s*[a-zA-Z]+)*)\)"
)


class IngredientLine(DBC, str):
    """Specify a well-formed line representing an ingredient list with the allergen."""

    @require(lambda line: INGREDIENT_LINE_RE.fullmatch(line))
    def __new__(cls, line: str) -> "IngredientLine":
        return cast(IngredientLine, line)


class Entry(DBC):
    """Represent an entry in the list of foods."""

    ingredients: List[Ingredient]  #: Ingredients of the entry
    allergens: List[Allergen]  #: Allergens of the entry

    @require(lambda allergens: len(allergens) > 0)
    @require(lambda ingredients: len(ingredients) > 0)
    def __init__(
        self, ingredients: List[Ingredient], allergens: List[Allergen]
    ) -> None:
        """Initialize with the given values."""
        self.ingredients = ingredients
        self.allergens = allergens


def parse_ingredient_line(line: IngredientLine) -> Entry:
    """Encapsulate the parsing of ``line`` into entries."""
    mtch = INGREDIENT_LINE_RE.fullmatch(line)

    # We have to manually do the splitting as the ``re`` module is not powerful
    # enough.

    assert mtch is not None, f"{line=}"
    ingredients_str = mtch.group("ingredients")
    ingredients = re.split(r"\s+", ingredients_str)

    allergens_str = mtch.group("allergens")
    allergens = re.split(r"\s*,\s*", allergens_str)

    # fmt: off
    return Entry(
        ingredients=[
            Ingredient(ingredient)
            for ingredient in ingredients
        ],
        allergens=[
            Allergen(allergen)
            for allergen in allergens
        ]
    )
    # fmt: on


# fmt: off
@ensure(
    lambda entry, result:
    result == serialize_entry(parse_ingredient_line(result))  # type: ignore
)
# fmt: on
def serialize_entry(entry: Entry) -> IngredientLine:
    """Serialize the ``entry`` back into the string."""
    ingredients_str = " ".join(ingredient for ingredient in entry.ingredients)
    allergens_str = ", ".join(allergen for allergen in entry.allergens)

    return IngredientLine(f"{ingredients_str} (contains {allergens_str})")


def find_non_allergenic_ingredients(entries: List[Entry]) -> Set[Ingredient]:
    """Find the ingredients without allergens."""
    # region Determine allergenic ingredients

    # Allergen 🠒 intersection of ingredients re-appearing for that allergen
    allergen_map = dict()  # type: MutableMapping[Allergen, Set[Ingredient]]

    for entry in entries:
        for allergen in entry.allergens:
            ingredient_intersection = allergen_map.get(allergen, None)

            if ingredient_intersection is None:
                allergen_map[allergen] = set(entry.ingredients)
            else:
                ingredient_intersection.intersection_update(entry.ingredients)

    allergenic_ingredients = set()  # type: Set[Ingredient]
    for ingredient_intersection in allergen_map.values():
        allergenic_ingredients.update(ingredient_intersection)

    # endregion

    # region Determine non-allergenic ingredients

    all_ingredients = set()  # type: Set[Ingredient]
    for entry in entries:
        all_ingredients.update(entry.ingredients)

    result = all_ingredients.difference(allergenic_ingredients)

    # endregion

    return result


def solve(lines: List[IngredientLine]) -> Set[Ingredient]:
    """Parse the input and return the set of ingredients without allergens."""

    entries = [parse_ingredient_line(line) for line in lines]

    return find_non_allergenic_ingredients(entries=entries)
