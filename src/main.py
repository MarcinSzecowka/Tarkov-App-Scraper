import links
from database import connect_to_mongo
from scrapers.items_scraper import fetch_and_save_items
from src.utils import remove_duplicates


def main():
    database = connect_to_mongo()
    articles = links.fetch_all_links()
    fetch_and_save_items(articles, database)
    remove_duplicates(database)


if __name__ == '__main__':
    main()
