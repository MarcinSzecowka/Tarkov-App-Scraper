from bs4 import BeautifulSoup


def weapon_category_parser(html):
    wiki_articles = []
    soup = BeautifulSoup(html.content, "lxml")
    for element in soup.find_all("a", {"class": "mw-redirect"}):
        if element.parent.name == "td" and element.get_text():
            wiki_articles.append(element["href"])
    return wiki_articles


def weapon_mod_category_parser(html):
    wiki_articles = []
    soup = BeautifulSoup(html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "td" and element.get_text():
            wiki_articles.append(element["href"])
    return wiki_articles


def basic_category_parser(html):
    wiki_articles = []
    soup = BeautifulSoup(html.content, "lxml")
    for element in soup.find_all("a"):
        if element.parent.name == "th" and element.get_text():
            wiki_articles.append(element["href"])
    return wiki_articles


def quests_list_parser(html):
    quest_links = []
    soup = BeautifulSoup(html.content, "lxml")
    for table_content in get_all_quest_wikitables(soup):
        rows = table_content.find_all("tr")
        for row in rows[2:]: # [2:] because we want to skip table headings
            a = row.find("th").find("b").find("a")
            if a:
                quest_links.append(a["href"])
    return quest_links


def get_all_quest_wikitables(soup):
    quest_wikitables = []
    all_wikitables = soup.find_all("table", {"class": "wikitable"})
    for wikitable in all_wikitables:
        table_classes = wikitable["class"]
        if is_content_table(table_classes):
            quest_wikitables.append(wikitable.find("tbody"))
    return quest_wikitables


def is_content_table(table_classes):
    return any("content" in table_class for table_class in table_classes)






















