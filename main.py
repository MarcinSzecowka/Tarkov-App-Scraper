import uuid

from bs4 import BeautifulSoup
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import pymongo

WIKI_LINK = "https://escapefromtarkov.fandom.com"


def parse_3(downloaded_html):
    parse_result = []
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a", {"class": "mw-redirect"}):
        if element.parent.name == "td" and element.get_text():
            parse_result.append(element["href"])
    return parse_result


def parse_2(downloaded_html):
    parse_result = []
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "td" and element.get_text():
            parse_result.append(element["href"])
    return parse_result


def parse_1(downloaded_html):
    parse_result = []
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            parse_result.append(element["href"])
    return parse_result


def get_all_items_links():
    all_items_links = []
    parse_1_candidates = ["/wiki/7.62x25mm_Tokarev", "/wiki/9x18mm_Makarov", "/wiki/9x19mm_Parabellum",
                          "/wiki/9x21mm_Gyurza", "/wiki/.45_ACP", "/wiki/4.6x30mm_HK", "/wiki/5.7x28mm_FN",
                          "/wiki/5.45x39mm", "/wiki/5.56x45mm_NATO", "/wiki/.300_Blackout", "/wiki/7.62x39mm",
                          "/wiki/7.62x51mm_NATO", "/wiki/7.62x54mmR", "/wiki/.338_Lapua_Magnum",
                          "/wiki/9x39mm", "/wiki/.366_TKM", "/wiki/12.7x55mm_STs-130", "/wiki/12.7x108mm"
                          "/wiki/12x70mm", "/wiki/20x70mm", "/wiki/23x75mm", "/wiki/30x29mm", "/wiki/40x46_mm"
                          "/wiki/Containers", "/wiki/Gear_components", "/wiki/Loot", "/wiki/Medical",
                          "/wiki/Provisions", "/wiki/Armbands", "/wiki/Armor_vests", "/wiki/Backpacks",
                          "/wiki/Chest_rigs", "/wiki/Eyewear", "/wiki/Face_cover", "/wiki/Headsets", "/wiki/Headwear",
                          "/wiki/Secure_containers", "/wiki/Tactical_clothing"]

    parse_2_candidates = ["/wiki/Keys_%26_Intel#Factory", "/wiki/Weapon_mods"]

    parse_3_candidates = ["/wiki/Weapons"]

    for ele in parse_1_candidates:
        all_items_links.append((WIKI_LINK + ele, parse_1))

    for ele in parse_2_candidates:
        all_items_links.append((WIKI_LINK + ele, parse_2))

    for ele in parse_3_candidates:
        all_items_links.append((WIKI_LINK + ele, parse_3))

    # return [(WIKI_LINK + "/wiki/Loot", parse_1)]
    return all_items_links


def get_rogue_links():
    # these didn't work while scraping so they had to be added manually
    leftover_links = ["/wiki/FN_GL40", "/wiki/6h5_Bayonet", "/wiki/Antique_axe", "/wiki/Bars_A-2607-_95x18",
                      "/wiki/Bars_A-2607-_Damascus", "/wiki/Camper_axe", "/wiki/Crash_Axe", "/wiki/Cultist%27s_knife",
                      "/wiki/ER_Fulcrum_Bayonet", "/wiki/Freeman_crowbar", "/wiki/Kiba_Arms_Tactical_Tomahawk",
                      "/wiki/Miller_Bros._Blades_M-2_Tactical_Sword", "/wiki/MPL-50_entrenching_tool",
                      "/wiki/Red_Rebel_Ice_pick", "/wiki/SP-8_Survival_Machete", "/wiki/UVSR_Taiga-1"]
    return leftover_links


def func_used_in_mapping(func_args):
    url = func_args[0]
    parsing_func = func_args[1]
    return parsing_func, requests.get(url)


def get_all_remaining_links():
    all_results = []
    with ThreadPoolExecutor(max_workers=2 * os.cpu_count() + 1) as pool:
        res = pool.map(func_used_in_mapping, elements_to_parse)
    for result in res:
        parsing_func = result[0]
        downloaded_html = result[1]
        for link in parsing_func(downloaded_html):
            all_results.append(link)
    return all_results


def database_declaration():
    # creating database
    username = "root"
    password = "rootpassword"
    my_client = pymongo.MongoClient("mongodb://localhost:27017/", username=username, password=password)
    my_db = my_client["Tarkov-app-db"]

    # delete collection if it already exists
    if "Items" in my_db.list_collection_names():
        items_collection = my_db["Items"]
        items_collection.drop()

    # creating collection
    items_collection = my_db["Items"]
    mapping_collection = my_db["mapping"]
    return items_collection, mapping_collection


def append_type(item, general_data_table):
    general_data_element = general_data_table.find_all("table", {"class": "va-infobox-group"})[1]
    all_general_data_tr = general_data_element.findChildren("tr")
    for tr in all_general_data_tr:
        all_td = tr.find_all("td")
        for td in all_td:
            if td.getText() == "Type":
                final_element = tr.find("td", {"class": "va-infobox-content"})
                if final_element.getText() is not None:
                    item["type"] = tr.find("td", {"class": "va-infobox-content"}).getText()
                    break
                else:
                    item["type"] = final_element.find("a")["href"]


def append_name(item, table):
    title = table.find("div", {"class": "va-infobox-title-main"})
    if title:
        item["name"] = title.getText()


def append_picture(item, table):
    picture = table.find("td", {"class": "va-infobox-mainimage-image"})
    if picture:
        item["picture"] = picture.find("a", href=True)["href"]


def append_icon(item, table):
    icon = table.find("td", {"class": "va-infobox-icon"})
    if icon:
        item["icon"] = icon.find("a", href=True)["href"]


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


def find_general_data_table(soup):
    return soup.find("table", {"class": "va-infobox"})


def append_quests(item, soup):
    all_h2_elements = soup.find_all("h2")
    for h2 in all_h2_elements:
        children = h2.find_all("span")
        for child in children:
            if child.getText() == "Quests":
                item["quests"] = []
                quests_element = h2.find_next_sibling()
                quests = quests_element.find_all("li")
                for quest in quests:
                    quest_dict = {}
                    quest_dict["trader"] = "Prapor"
                    all_quest_hrefs = quest.find_all("a", href=True)
                    if all_quest_hrefs[0]["href"] == "/wiki/Found_in_raid":
                        quest_dict["name"] = all_quest_hrefs[1].getText()
                        quest_dict["foundInRaidRequired"] = True
                    else:
                        quest_dict["name"] = all_quest_hrefs[0].getText()
                        quest_dict["foundInRaidRequired"] = False
                    try:
                        # quest_dict["itemCount"] = int(quest.getText().split(" ", 0)[0])
                        quest_dict["itemCount"] = int(quest.getText().split(" ", 1)[0])
                    except ValueError:
                        pass
                    item["quests"].append(quest_dict)
                else:
                    break


def is_crafting_table(table):
    prev_sibling = table.find_previous_sibling()
    header = prev_sibling.find("span", {"id": "Crafting"})
    return header and header.getText() == "Crafting"


def find_all_links_without_children(table_header):
    links = table_header.find_all("a")
    return list(filter(lambda link: not link.find("img"), links))


def parse_component_count(item_component_name, full_text):
    split = full_text.strip().split("+")
    for word in split:
        if item_component_name in word:
            count_text = word.strip().removesuffix(item_component_name)
            return count_text.removeprefix("x").strip()
    return None


def parse_component_image(table_header, link):
    link_with_image = table_header.find("a", {"title": link.getText()})
    if link_with_image:
        image = link_with_image.find("img")
        if image:
            data_src = image.get("data-src")
            src = image.get("src")
            if data_src:
                return data_src
            elif src:
                return src
    return None


def fetch_item_id_from_database(item_component_name):
    mapping = mapping_collection.find_one({"name": item_component_name})
    if mapping:
        return mapping["id"]
    return "undefined"


def parse_item_component(link, full_text):
    item_component = {}
    item_component_name = link.getText()
    item_component["name"] = item_component_name
    item_component["count"] = parse_component_count(item_component_name, full_text)
    item_component["id"] = fetch_item_id_from_database(item_component_name)
    return item_component


def parse_item_components(table_header):
    components = []
    full_text = table_header.getText()
    links = find_all_links_without_children(table_header)
    for link in links:
        component = parse_item_component(link, full_text)
        components.append(component)
    return components


def parse_hideout_module(table_header):
    hideout_module = {}
    link = table_header.find("a")
    if link:
        text = link.getText().strip().split("level")
        hideout_module["name"] = text[0].strip()
        hideout_module["level"] = text[1].strip()
    hideout_module["time"] = table_header.find("br").next.getText().strip()
    return hideout_module


def parse_crafting_recipe(row):
    crafting_recipe = {}
    table_headers = row.find_all("th")
    if len(table_headers) != 5:
        print(f"Unable to parse crafting recipe for row: {row.getText()}")
        return None

    components = parse_item_components(table_headers[0])
    products = parse_item_components(table_headers[4])
    hideout_module = parse_hideout_module(table_headers[2])

    crafting_recipe["id"] = str(uuid.uuid4())
    crafting_recipe["components"] = components
    crafting_recipe["product"] = products[0]
    crafting_recipe["module"] = hideout_module["name"]
    crafting_recipe["level"] = hideout_module["level"]
    crafting_recipe["time"] = hideout_module["time"]

    return crafting_recipe


def append_crafting_recipes(item, soup):
    crafting_recipes = []

    wikitables = soup.find_all("table", {"class": "wikitable"})
    if wikitables:
        for table in wikitables:
            if is_crafting_table(table):
                rows = table.find("tbody").find_all("tr")
                for row in rows:
                    try:
                        recipe = parse_crafting_recipe(row)
                        if recipe:
                            crafting_recipes.append(recipe)
                    except IndexError:
                        print(f'Failed to parse crafting recipe for {item["name"]}')

    if crafting_recipes:
        item["crafting"] = crafting_recipes


def append_id(item):
    mapping = mapping_collection.find_one({"name": item["name"]})
    if mapping:
        item["id"] = mapping["id"]


def parse_item(html):
    item = {}
    soup = BeautifulSoup(html.content, "lxml")

    if not find_general_data_table(soup):
        item["name"] = get_page_title(soup)
        return item

    append_general_data(item, soup)
    append_id(item)
    append_quests(item, soup)
    append_crafting_recipes(item, soup)

    return item


def get_page_title(soup):
    return soup.find("h1", {"class": "page-header__title"}).getText()


def get_all_items_responses(links_set):
    item_dicts = []
    fails = []
    with ThreadPoolExecutor(max_workers=2 * os.cpu_count() + 1) as pool:
        res = pool.map(requests.get, links_set)
    for result in res:
        item = parse_item(result)
        if item:
            if isinstance(item, dict):
                item_dicts.append(item)
            else:
                fails.append(item)
    return item_dicts, fails


if __name__ == '__main__':
    # creating database
    items_collection, mapping_collection = database_declaration()

    # getting all links
    elements_to_parse = get_all_items_links()
    parsing_results = get_all_remaining_links()
    rogue_links = get_rogue_links()
    parsing_results.extend(rogue_links)

    # removing None types
    parsing_results = [WIKI_LINK + ele for ele in parsing_results if ele is not None]

    # removing duplicates
    parsing_results = set(parsing_results)

    # scraping item info from links
    items_dicts_list, fails_list = get_all_items_responses(parsing_results)

    # checking all fails
    for y in fails_list:
        print(f"Failed in: {y}")

    # checking the number of items and fails
    print(f"Item count: {len(items_dicts_list)}")
    print(f"Fail count: {len(fails_list)}")

    # inserting all scraped items into the "Items" collection
    print(items_collection.insert_many(items_dicts_list).inserted_ids)
