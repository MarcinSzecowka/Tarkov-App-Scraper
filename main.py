from bs4 import BeautifulSoup
import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor

WIKI_LINK = "https://escapefromtarkov.fandom.com"


def parse_3(downloaded_html):
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a", {"class": "mw-redirect"}):
        if element.parent.name == "td" and element.get_text():
            parsing_results.append(element["href"])


def parse_2(downloaded_html):
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "td" and element.get_text():
            parsing_results.append(element["href"])


def parse_1(downloaded_html):
    soup = BeautifulSoup(downloaded_html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            parsing_results.append(element["href"])


def get_all_gear_links():
    # Armbands
    url = WIKI_LINK + "/wiki/Armbands"
    elements_to_parse.append((url, parse_1))

    # Armor vests
    url = WIKI_LINK + "/wiki/Armor_vests"
    elements_to_parse.append((url, parse_1))

    # Backpacks
    url = WIKI_LINK + "/wiki/Backpacks"
    elements_to_parse.append((url, parse_1))

    # Chest rigs
    url = WIKI_LINK + "/wiki/Chest_rigs"
    elements_to_parse.append((url, parse_1))

    # Eye wear
    url = WIKI_LINK + "/wiki/Eyewear"
    elements_to_parse.append((url, parse_1))

    # Face cover
    url = WIKI_LINK + "/wiki/Face_cover"
    elements_to_parse.append((url, parse_1))

    # Head sets
    url = WIKI_LINK + "/wiki/Headsets"
    elements_to_parse.append((url, parse_1))

    # Head wear
    url = WIKI_LINK + "/wiki/Headwear"
    elements_to_parse.append((url, parse_1))

    # Secure containers
    url = WIKI_LINK + "/wiki/Secure_containers"
    elements_to_parse.append((url, parse_1))

    # Tactical clothing
    url = WIKI_LINK + "/wiki/Tactical_clothing"
    elements_to_parse.append((url, parse_1))

    # Weapons
    url = WIKI_LINK + "/wiki/Weapons"
    elements_to_parse.append((url, parse_3))

    # add grenade launchers
    # add melee
    # because they cannot be scraped for some reason
    leftover_links = ["/wiki/FN_GL40", "/wiki/6h5_Bayonet", "/wiki/Antique_axe", "/wiki/Bars_A-2607-_95x18",
                      "/wiki/Bars_A-2607-_Damascus", "/wiki/Camper_axe", "/wiki/Crash_Axe", "/wiki/Cultist%27s_knife",
                      "/wiki/ER_Fulcrum_Bayonet", "/wiki/Freeman_crowbar", "/wiki/Kiba_Arms_Tactical_Tomahawk",
                      "/wiki/Miller_Bros._Blades_M-2_Tactical_Sword", "/wiki/MPL-50_entrenching_tool",
                      "/wiki/Red_Rebel_Ice_pick", "/wiki/SP-8_Survival_Machete", "/wiki/UVSR_Taiga-1"]

    parsing_results.extend(leftover_links)


def get_all_items_links():
    # Ammunition

    # 7.62x25mm_Tokarev
    url = WIKI_LINK + "/wiki/7.62x25mm_Tokarev"
    elements_to_parse.append((url, parse_1))

    # 9x18mm_Makarov
    url = WIKI_LINK + "/wiki/9x18mm_Makarov"
    elements_to_parse.append((url, parse_1))

    # 9x19mm_Parabellum
    url = WIKI_LINK + "/wiki/9x19mm_Parabellum"
    elements_to_parse.append((url, parse_1))

    # 9x21mm_Gyurza
    url = WIKI_LINK + "/wiki/9x21mm_Gyurza"
    elements_to_parse.append((url, parse_1))

    # .45_ACP
    url = WIKI_LINK + "/wiki/.45_ACP"
    elements_to_parse.append((url, parse_1))

    # 4.6x30mm_HK
    url = WIKI_LINK + "/wiki/4.6x30mm_HK"
    elements_to_parse.append((url, parse_1))

    # 5.7x28mm_FN
    url = WIKI_LINK + "/wiki/5.7x28mm_FN"
    elements_to_parse.append((url, parse_1))

    # 5.45x39mm
    url = WIKI_LINK + "/wiki/5.45x39mm"
    elements_to_parse.append((url, parse_1))

    # 5.56x45mm_NATO
    url = WIKI_LINK + "/wiki/5.56x45mm_NATO"
    elements_to_parse.append((url, parse_1))

    # .300_Blackout
    url = WIKI_LINK + "/wiki/.300_Blackout"
    elements_to_parse.append((url, parse_1))

    # 7.62x39mm
    url = WIKI_LINK + "/wiki/7.62x39mm"
    elements_to_parse.append((url, parse_1))

    # 7.62x51mm_NATO
    url = WIKI_LINK + "/wiki/7.62x51mm_NATO"
    elements_to_parse.append((url, parse_1))

    # 7.62x54mmR
    url = WIKI_LINK + "/wiki/7.62x54mmR"
    elements_to_parse.append((url, parse_1))

    # .338_Lapua_Magnum
    url = WIKI_LINK + "/wiki/.338_Lapua_Magnum"
    elements_to_parse.append((url, parse_1))

    # 9x39mm
    url = WIKI_LINK + "/wiki/9x39mm"
    elements_to_parse.append((url, parse_1))

    # .366_TKM
    url = WIKI_LINK + "/wiki/.366_TKM"
    elements_to_parse.append((url, parse_1))

    # 12.7x55mm_STs-130
    url = WIKI_LINK + "/wiki/12.7x55mm_STs-130"
    elements_to_parse.append((url, parse_1))

    # 12.7x108mm
    url = WIKI_LINK + "/wiki/12.7x108mm"
    elements_to_parse.append((url, parse_1))

    # 12x70mm
    url = WIKI_LINK + "/wiki/12x70mm"
    elements_to_parse.append((url, parse_1))

    # 20x70mm
    url = WIKI_LINK + "/wiki/20x70mm"
    elements_to_parse.append((url, parse_1))

    # 23x75mm
    url = WIKI_LINK + "/wiki/23x75mm"
    elements_to_parse.append((url, parse_1))

    # 30x29mm
    url = WIKI_LINK + "/wiki/30x29mm"
    elements_to_parse.append((url, parse_1))

    # 40x46_mm
    url = WIKI_LINK + "/wiki/40x46_mm"
    elements_to_parse.append((url, parse_1))

    # End of Ammunition
    ##################################################################################

    # Containers
    url = WIKI_LINK + "/wiki/Containers"
    elements_to_parse.append((url, parse_1))

    # Gear_components
    url = WIKI_LINK + "/wiki/Gear_components"
    elements_to_parse.append((url, parse_1))

    # All keys, ignore the wiki link, it scrapes everything
    url = WIKI_LINK + "/wiki/Keys_%26_Intel#Factory"
    elements_to_parse.append((url, parse_2))

    # Loot
    url = WIKI_LINK + "/wiki/Loot"
    elements_to_parse.append((url, parse_1))

    # Medical
    url = WIKI_LINK + "/wiki/Medical"
    elements_to_parse.append((url, parse_1))

    # Provisions
    url = WIKI_LINK + "/wiki/Provisions"
    elements_to_parse.append((url, parse_1))

    # Weapon_mods
    url = WIKI_LINK + "/wiki/Weapon_mods"
    elements_to_parse.append((url, parse_2))


def func_used_in_mapping(func_args):
    url = func_args[0]
    parsing_func = func_args[1]
    return parsing_func, requests.get(url)


def main():
    with ThreadPoolExecutor(max_workers=2 * os.cpu_count() + 1) as pool:
        res = pool.map(
            func_used_in_mapping,
            elements_to_parse
        )
    for result in res:
        parsing_func = result[0]
        downloaded_html = result[1]
        parsing_results.append(parsing_func(downloaded_html))


if __name__ == '__main__':
    parsing_results = []
    elements_to_parse = []
    get_all_gear_links()
    get_all_items_links()
    main()
    parsing_results = [ele for ele in parsing_results if ele is not None]
    parsing_results = set(parsing_results)
