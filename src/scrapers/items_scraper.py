from concurrent.futures import ThreadPoolExecutor

from src.database import get_collections
from src.parsers.item.items_parser import parse_item
from src.scrapers.scraping_utils import filter_already_downloaded_items, try_fetch, group_results, save_download
from src.utils import max_workers


def save_item(item, url, items_collection):
    item["wiki_link"] = url
    item["type"] = "item"
    items_collection.insert_one(item)


def parse_and_save_items(successful_requests, items_collection, downloads_collection, mapping_collection):
    unparseable_items = []
    for successful_request in successful_requests:
        article, url = successful_request
        item = parse_item(article, mapping_collection)
        if isinstance(item, dict):
            save_download(url, "item", downloads_collection)
            save_item(item, url, items_collection)
        else:
            unparseable_items.append(item)
    return unparseable_items


def fetch_and_save_items(articles, database):
    items_collection, mapping_collection, downloads_collection = get_collections(database)
    print(f'Fetching items. Items to fetch: {len(articles)}')

    filtered = filter_already_downloaded_items(articles, downloads_collection)
    print(f'{len(articles) - len(filtered)} quests have already been downloaded, skipping. New quests to download: {len(filtered)}')

    with ThreadPoolExecutor(max_workers=max_workers()) as pool:
        fetch_results = pool.map(try_fetch, filtered)

    failed_requests, successful_requests = group_results(fetch_results)
    unparseable_items = parse_and_save_items(successful_requests, items_collection, downloads_collection, mapping_collection)

    failures = failed_requests + unparseable_items
    print(f'Finished data fetching process. Failures: {len(failures)}')
    print(failures)
