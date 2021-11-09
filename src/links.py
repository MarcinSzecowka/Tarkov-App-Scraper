from parsers.category_parsers import weapon_category_parser, basic_category_parser, weapon_mod_category_parser
from scrapers.articles_scraper import fetch_remaining_articles

# these didn't work while scraping so they had to be added manually
WIKI_LINK = "https://escapefromtarkov.fandom.com"
ROGUE_ARTICLES = ["/wiki/FN_GL40", "/wiki/6Kh5_Bayonet", "/wiki/Antique_axe", "/wiki/Bars_A-2607_-_95x18_knife",
                  "/wiki/Bars_A-2607_Damascus_knife", "/wiki/Camper_axe", "/wiki/Crash_Axe", "/wiki/Cultist_knife",
                  "/wiki/ER_FULCRUM_BAYONET", "/wiki/Freeman_crowbar", "/wiki/Kiba_Arms_Tactical_Tomahawk",
                  "/wiki/Miller_Bros._Blades_M-2_Tactical_Sword", "/wiki/MPL-50_entrenching_tool",
                  "/wiki/Red_Rebel_ice_pick", "/wiki/SP-8_Survival_Machete", "/wiki/UVSR_Taiga-1_survival_machete"]


def fetch_all_links():
    categories_and_parsers = get_categories_and_parsers()
    articles = fetch_remaining_articles(categories_and_parsers)
    articles.extend(ROGUE_ARTICLES)
    articles = remove_none_types(articles)
    articles = append_protocol_and_domain(articles)
    return list(set(articles))


def get_categories_and_parsers():
    categories_and_parsers = []
    basic_item_links = ["/wiki/7.62x25mm_Tokarev", "/wiki/9x18mm_Makarov", "/wiki/9x19mm_Parabellum",
                        "/wiki/9x21mm_Gyurza", "/wiki/.45_ACP", "/wiki/4.6x30mm_HK", "/wiki/5.7x28mm_FN",
                        "/wiki/5.45x39mm", "/wiki/5.56x45mm_NATO", "/wiki/.300_Blackout", "/wiki/7.62x39mm",
                        "/wiki/7.62x51mm_NATO", "/wiki/7.62x54mmR", "/wiki/.338_Lapua_Magnum",
                        "/wiki/9x39mm", "/wiki/.366_TKM", "/wiki/12.7x55mm_STs-130", "/wiki/12.7x108mm"
                        "/wiki/12x70mm", "/wiki/20x70mm", "/wiki/23x75mm", "/wiki/30x29mm", "/wiki/40x46_mm"
                        "/wiki/Containers", "/wiki/Gear_components", "/wiki/Loot", "/wiki/Medical",
                        "/wiki/Provisions", "/wiki/Armbands", "/wiki/Armor_vests", "/wiki/Backpacks",
                        "/wiki/Chest_rigs", "/wiki/Eyewear", "/wiki/Face_cover", "/wiki/Headsets", "/wiki/Headwear",
                        "/wiki/Secure_containers", "/wiki/Tactical_clothing"]

    weapon_mod_links = ["/wiki/Keys_%26_Intel#Factory", "/wiki/Weapon_mods"]

    weapon_links = ["/wiki/Weapons"]

    for basic_item_link in basic_item_links:
        categories_and_parsers.append((WIKI_LINK + basic_item_link, basic_category_parser))

    for weapon_mod_link in weapon_mod_links:
        categories_and_parsers.append((WIKI_LINK + weapon_mod_link, weapon_mod_category_parser))

    for weapon_link in weapon_links:
        categories_and_parsers.append((WIKI_LINK + weapon_link, weapon_category_parser))

    # return [(WIKI_LINK + "/wiki/Medical", basic_category_parser)]
    return categories_and_parsers


def remove_none_types(articles):
    return [article for article in articles if article is not None]


def append_protocol_and_domain(articles):
    return [WIKI_LINK + article for article in articles if article]
