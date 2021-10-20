from bs4 import BeautifulSoup
import requests

WIKI_LINK = "https://escapefromtarkov.fandom.com"


def get_all_gear_links():
    all_gear_links_inner = set()

    # Armbands
    url = WIKI_LINK + "/wiki/Armbands"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            all_gear_links_inner.add(element["href"])

    # Armor vests
    url = WIKI_LINK + "/wiki/Armor_vests"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Backpacks
    url = WIKI_LINK + "/wiki/Backpacks"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Chest rigs
    url = WIKI_LINK + "/wiki/Chest_rigs"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Eye wear
    url = WIKI_LINK + "/wiki/Eyewear"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Face cover
    url = WIKI_LINK + "/wiki/Face_cover"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Head sets
    url = WIKI_LINK + "/wiki/Headsets"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Head wear
    url = WIKI_LINK + "/wiki/Headwear"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Secure containers
    url = WIKI_LINK + "/wiki/Secure_containers"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Tactical clothing
    url = WIKI_LINK + "/wiki/Tactical_clothing"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # Weapons
    url = WIKI_LINK + "/wiki/Weapons"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a", {"class": "mw-redirect"}):
        if element.parent.name == "td" and element.get_text():
            # print(element["href"])
            all_gear_links_inner.add(element["href"])

    # add grenade launchers
    # add melee
    piece_of_shit = ["/wiki/FN_GL40", "/wiki/6h5_Bayonet", "/wiki/Antique_axe", "/wiki/Bars_A-2607-_95x18",
                     "/wiki/Bars_A-2607-_Damascus", "/wiki/Camper_axe", "/wiki/Crash_Axe", "/wiki/Cultist%27s_knife",
                     "/wiki/ER_Fulcrum_Bayonet", "/wiki/Freeman_crowbar", "/wiki/Kiba_Arms_Tactical_Tomahawk",
                     "/wiki/Miller_Bros._Blades_M-2_Tactical_Sword", "/wiki/MPL-50_entrenching_tool",
                     "/wiki/Red_Rebel_Ice_pick", "/wiki/SP-8_Survival_Machete", "/wiki/UVSR_Taiga-1"]
    # because they cannot be scraped for some reason
    for x in piece_of_shit:
        all_gear_links_inner.add(x)
    return all_gear_links_inner


def get_all_items_links():
    all_items_links_inner = set()

    # Ammunition

    # 7.62x25mm_Tokarev
    url = WIKI_LINK + "/wiki/7.62x25mm_Tokarev"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 9x18mm_Makarov
    url = WIKI_LINK + "/wiki/9x18mm_Makarov"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 9x19mm_Parabellum
    url = WIKI_LINK + "/wiki/9x19mm_Parabellum"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 9x21mm_Gyurza
    url = WIKI_LINK + "/wiki/9x21mm_Gyurza"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # .45_ACP
    url = WIKI_LINK + "/wiki/.45_ACP"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 4.6x30mm_HK
    url = WIKI_LINK + "/wiki/4.6x30mm_HK"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 5.7x28mm_FN
    url = WIKI_LINK + "/wiki/5.7x28mm_FN"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 5.45x39mm
    url = WIKI_LINK + "/wiki/5.45x39mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 5.56x45mm_NATO
    url = WIKI_LINK + "/wiki/5.56x45mm_NATO"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # .300_Blackout
    url = WIKI_LINK + "/wiki/.300_Blackout"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 7.62x39mm
    url = WIKI_LINK + "/wiki/7.62x39mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 7.62x51mm_NATO
    url = WIKI_LINK + "/wiki/7.62x51mm_NATO"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 7.62x54mmR
    url = WIKI_LINK + "/wiki/7.62x54mmR"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # .338_Lapua_Magnum
    url = WIKI_LINK + "/wiki/.338_Lapua_Magnum"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 9x39mm
    url = WIKI_LINK + "/wiki/9x39mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # .366_TKM
    url = WIKI_LINK + "/wiki/.366_TKM"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 12.7x55mm_STs-130
    url = WIKI_LINK + "/wiki/12.7x55mm_STs-130"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 12.7x108mm
    url = WIKI_LINK + "/wiki/12.7x108mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 12x70mm
    url = WIKI_LINK + "/wiki/12x70mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 20x70mm
    url = WIKI_LINK + "/wiki/20x70mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 23x75mm
    url = WIKI_LINK + "/wiki/23x75mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 30x29mm
    url = WIKI_LINK + "/wiki/30x29mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # 40x46_mm
    url = WIKI_LINK + "/wiki/40x46_mm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # End of Ammunition
    ##################################################################################

    # Containers
    url = WIKI_LINK + "/wiki/Containers"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # Gear_components
    url = WIKI_LINK + "/wiki/Gear_components"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # All keys, ignore the wiki link, it scrapes everything
    url = WIKI_LINK + "/wiki/Keys_%26_Intel#Factory"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "td" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # Loot
    url = WIKI_LINK + "/wiki/Loot"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # Medical
    url = WIKI_LINK + "/wiki/Medical"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # Provisions
    url = WIKI_LINK + "/wiki/Provisions"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    # Weapon_mods
    url = WIKI_LINK + "/wiki/Weapon_mods"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "td" and element.get_text():
            # print(element["href"])
            all_items_links_inner.add(element["href"])

    return all_items_links_inner


if __name__ == '__main__':
    all_gear_links = get_all_gear_links()
    # print(len(all_gear_links))
    #########################################
    all_items_links = get_all_items_links()
    # print(len(all_items_links))
    #########################################
    every_item_link = set.union(all_gear_links, all_items_links)
    print(len(every_item_link))
    pass
