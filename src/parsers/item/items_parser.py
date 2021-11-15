from bs4 import BeautifulSoup

from src.parsers.item.barter_trades_parser import append_barter_trades
from src.parsers.item.crafting_recipes_parser import append_crafting_recipes
from src.parsers.item.item_quests_parser import append_quests
from src.parsers.parser_utils import find_general_data_table, get_page_title


def parse_item(html, mapping_collection):
    item = {}
    soup = BeautifulSoup(html.content, "lxml")

    if not find_general_data_table(soup):
        item["name"] = get_page_title(soup)
        return item

    append_general_data(item, soup)
    append_id(item, mapping_collection)
    append_quests(item, soup)
    append_crafting_recipes(item, soup, mapping_collection)
    append_barter_trades(item, soup, mapping_collection)

    return item


def append_general_data(item, soup):
    table = find_general_data_table(soup)
    if not table:
        return
    try:
        append_type(item, table)
        append_name(item, table)
        append_picture(item, table)
        append_icon(item, table)
        append_sold_by(item, table)
    except IndexError:
        pass


def append_id(item, mapping_collection):
    item_name = item.get("name")
    if item_name:
        mapping = mapping_collection.find_one({"name": item_name})
        if mapping:
            item["id"] = mapping["id"]
    else:
        print(f'Item {item} has no name, aborting append_id')


def append_type(item, general_data_table):
    general_data_element = general_data_table.find_all("table", {"class": "va-infobox-group"})[1]
    all_general_data_tr = general_data_element.findChildren("tr")
    for tr in all_general_data_tr:
        all_td = tr.find_all("td")
        for td in all_td:
            if td.getText() == "Type":
                final_element = tr.find("td", {"class": "va-infobox-content"})
                if final_element.getText() is not None:
                    item["type"] = tr.find("td", {"class": "va-infobox-content"}).getText().strip()
                    break
                else:
                    item["type"] = final_element.find("a")["href"].strip()


def append_name(item, table):
    title = table.find("div", {"class": "va-infobox-title-main"})
    if title:
        item["name"] = title.getText().strip()


def append_picture(item, table):
    picture = table.find("td", {"class": "va-infobox-mainimage-image"})
    if picture:
        item["picture"] = picture.find("a", href=True)["href"]


def append_icon(item, table):
    icon = table.find("td", {"class": "va-infobox-icon"})
    if icon:
        item["icon"] = icon.find("a", href=True)["href"]


def append_sold_by(item, table):
    sold_by = []
    table_data_cells = table.find_all("td", {"class": "va-infobox-label"})
    for td in table_data_cells:
        if "Sold by".lower() in td.getText().lower():
            trader_tds = td.find_next_siblings("td", {"class": "va-infobox-content"})
            for trader_td in trader_tds:
                text = trader_td.getText().strip()
                split = text.split(" ")
                sold_by.append({
                    "trader": split[0],
                    "level": split[1].removeprefix("LL").strip()
                })
    if sold_by:
        item["soldBy"] = sold_by

