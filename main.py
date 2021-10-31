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
    # if "Items" in my_db.list_collection_names():
    #     my_col = my_db["Items"]
    #     my_col.drop()

    # creating collection
    my_col = my_db["Items"]
    return my_col


def parsing_items_function(downloaded_html):
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    try:
        item_dict = {}
        if soup.find("table", {"class": "va-infobox"}):
            table = soup.find("table", {"class": "va-infobox"})
            # general info table
            try:
                general_data_element = table.find_all("table", {"class": "va-infobox-group"})[1]
                # type
                all_general_data_tr = general_data_element.findChildren("tr")
                for tr in all_general_data_tr:
                    all_td = tr.find_all("td")
                    for td in all_td:
                        if td.getText() == "Type":
                            final_element = tr.find("td", {"class": "va-infobox-content"})
                            if final_element.getText() is not None:
                                item_dict["type"] = tr.find("td", {"class": "va-infobox-content"}).getText()
                                break
                            else:
                                item_dict["type"] = final_element.find("a")["href"]
            except IndexError:
                pass
            # title

            if table.find("div", {"class": "va-infobox-title-main"}):
                title = table.find("div", {"class": "va-infobox-title-main"}).getText()
                item_dict["name"] = title
            # icon
            if table.find("td", {"class": "va-infobox-icon"}):
                icon_element = table.find("td", {"class": "va-infobox-icon"})
                icon_link = icon_element.find("a", href=True)["href"]
                item_dict["image"] = icon_link
        if item_dict:
            return item_dict
        else:
            return None
    except AttributeError:
        item_dict = soup.find("h1", {"class": "page-header__title"}).getText()
        return item_dict


def try_get(url):
    try:
        return requests.get(url, timeout=10)
    except Exception as e:
        return e


def get_all_items_responses(links_set, collection):
    fails = []
    with ThreadPoolExecutor(max_workers=2 * os.cpu_count() + 1) as pool:
        res = pool.map(try_get, links_set)
    for result in res:
        if isinstance(result, Exception):
            fails.append(result)
        else:
            item = parsing_items_function(result)
            if item:
                if isinstance(item, dict):
                    collection.insert_one(item)
                else:
                    fails.append(item)
    return fails


if __name__ == '__main__':
    # creating database
    items_collection = database_declaration()

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
    fails_list = get_all_items_responses(list(parsing_results)[0:1000], items_collection)

    # checking all fails
    for y in fails_list:
        print(f"Failed in: {y}")

    # checking the number of fails
    print(f"Fail count: {len(fails_list)}")
