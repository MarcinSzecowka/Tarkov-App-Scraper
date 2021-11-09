import uuid

from src.parsers.item_components_parser import parse_item_components


def append_barter_trades(item, soup, mapping_collection):
    barter_trades = []

    wikitables = soup.find_all("table", {"class": "wikitable"})
    if wikitables:
        for table in wikitables:
            if is_barter_table(table):
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    try:
                        recipe = parse_barter_trade(row, mapping_collection)
                        if recipe:
                            barter_trades.append(recipe)
                    except IndexError:
                        print(f'Failed to parse crafting recipe for {item["name"]}')

    if barter_trades:
        item["barters"] = barter_trades


def is_barter_table(table):
    prev_sibling = table.find_previous_sibling()
    header = prev_sibling.find("span", {"id": "Trading"})
    return header and header.getText() == "Trading"


def parse_barter_trade(row, mapping_collection):
    barter_trade = {}
    table_headers = row.find_all("th")
    if len(table_headers) != 5:
        print(f"Unable to parse crafting recipe for row: {row.getText()}")
        return None

    components = parse_item_components(table_headers[0], mapping_collection)
    products = parse_item_components(table_headers[4], mapping_collection)
    trader = parse_trader(table_headers[2])

    barter_trade["id"] = str(uuid.uuid4())
    barter_trade["requiredItems"] = components
    barter_trade["product"] = products[0]
    barter_trade["trader"] = trader["name"]
    barter_trade["level"] = trader["level"]

    return barter_trade


def parse_trader(table_header):
    text = table_header.getText().strip()
    split = text.split(" ")
    return {
        "name": split[0],
        "level": split[1].removeprefix("LL")
    }
