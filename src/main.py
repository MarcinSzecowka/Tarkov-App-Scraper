import items_links
from database import connect_to_mongo
from scrapers.items_scraper import fetch_and_save_items
from src import quests_links
from src.parsers.item.items_utils import remove_duplicated_items
from src.parsers.quests.quests_utils import add_item_ids_to_quest_rewards, add_quests_ids_to_prev_and_next_fields
from src.scrapers.quests_scraper import fetch_and_save_quests


def main():
    database = connect_to_mongo()
    # fetch_items(database)
    fetch_quests(database)


def fetch_quests(database):
    quests_articles = quests_links.fetch_all_quests_links()
    fetch_and_save_quests(quests_articles, database)
    add_quests_ids_to_prev_and_next_fields(database)
    add_item_ids_to_quest_rewards(database)


def fetch_items(database):
    item_articles = items_links.fetch_all_items_links()
    fetch_and_save_items(item_articles, database)
    remove_duplicated_items(database)


if __name__ == '__main__':
    main()
