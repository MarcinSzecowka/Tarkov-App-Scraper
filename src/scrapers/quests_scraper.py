from concurrent.futures import ThreadPoolExecutor

from src.database import get_collections
from src.parsers.quests.quests_parser import parse_quest
from src.scrapers.scraping_utils import filter_already_downloaded_items, try_fetch, group_results, save_download
from src.utils import max_workers


def fetch_and_save_quests(articles, database):
    _, _, downloads_collection, quests_collection = get_collections(database)
    print(f'Fetching quests. Quests to fetch: {len(articles)}')

    filtered = filter_already_downloaded_items(articles, downloads_collection)
    print(
        f'{len(articles) - len(filtered)} items have already been downloaded, skipping. New items to download: {len(filtered)}')

    with ThreadPoolExecutor(max_workers=max_workers()) as pool:
        fetch_results = pool.map(try_fetch, filtered)

    failed_requests, successful_requests = group_results(fetch_results)
    unparseable_items = parse_and_save_quests(successful_requests, quests_collection, downloads_collection)

    failures = failed_requests + unparseable_items
    print(f'Finished data fetching process. Failures: {len(failures)}')
    print(failures)


def save_quest(quest, url, quests_collection):
    quest["wiki_link"] = url
    quest["type"] = "quest"
    quests_collection.insert_one(quest)


def parse_and_save_quests(successful_requests, quests_collection, downloads_collection):
    unparseable_items = []
    for successful_request in successful_requests:
        article, url = successful_request
        quest = parse_quest(article)
        if isinstance(quest, dict):
            save_download(url, "quest", downloads_collection)
            save_quest(quest, url, quests_collection)
        else:
            unparseable_items.append(quest)
    return unparseable_items
