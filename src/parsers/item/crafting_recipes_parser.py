import uuid

from src.parsers.item.hideout_parser import parse_hideout_module
from src.parsers.item.item_components_parser import parse_item_components


def append_crafting_recipes(item, soup, mapping_collection):
    crafting_recipes = []

    wikitables = soup.find_all("table", {"class": "wikitable"})
    if wikitables:
        for table in wikitables:
            if is_crafting_table(table):
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    try:
                        recipe = parse_crafting_recipe(row, mapping_collection)
                        if recipe:
                            crafting_recipes.append(recipe)
                    except IndexError:
                        print(f'Failed to parse crafting recipe for {item["name"]}')

    if crafting_recipes:
        item["crafting"] = crafting_recipes


def is_crafting_table(table):
    prev_sibling = table.find_previous_sibling()
    header = prev_sibling.find("span", {"id": "Crafting"})
    return header and header.getText() == "Crafting"


def parse_crafting_recipe(row, mapping_collection):
    crafting_recipe = {}
    table_headers = row.find_all("th")
    if len(table_headers) != 5:
        print(f"Unable to parse crafting recipe for row: {row.getText()}")
        return None

    components = parse_item_components(table_headers[0], mapping_collection)
    products = parse_item_components(table_headers[4], mapping_collection)
    hideout_module = parse_hideout_module(table_headers[2])

    crafting_recipe["id"] = str(uuid.uuid4())
    crafting_recipe["components"] = components
    crafting_recipe["product"] = products[0]
    crafting_recipe["module"] = hideout_module["name"]
    crafting_recipe["level"] = hideout_module["level"]
    crafting_recipe["time"] = hideout_module["time"]

    return crafting_recipe
