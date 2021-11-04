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
