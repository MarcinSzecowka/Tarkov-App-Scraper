import items_links
from database import connect_to_mongo
from scrapers.items_scraper import fetch_and_save_items
from src import quests_links
from src.scrapers.quests_scraper import fetch_and_save_quests
from src.utils import remove_duplicates


def main():
    database = connect_to_mongo()
    # fetch_items(database)
    fetch_quests(database)
    # remove_duplicates(database)


def fetch_quests(database):
    quests_articles = quests_links.fetch_all_quests_links()
    fetch_and_save_quests(quests_articles, database)


def fetch_items(database):
    item_articles = items_links.fetch_all_items_links()
    fetch_and_save_items(item_articles, database)


if __name__ == '__main__':
    main()
