from bs4 import BeautifulSoup

from src.parsers.crafting_recipes_parser import append_crafting_recipes
from src.parsers.quests_parser import append_quests


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

    return item


def find_general_data_table(soup):
    return soup.find("table", {"class": "va-infobox"})


def get_page_title(soup):
    return soup.find("h1", {"class": "page-header__title"}).getText()


def append_general_data(item, soup):
    table = find_general_data_table(soup)
    if not table:
        return
    try:
        append_type(item, table)
        append_name(item, table)
        append_picture(item, table)
        append_icon(item, table)
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

