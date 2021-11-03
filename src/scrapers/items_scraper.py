import datetime
from concurrent.futures import ThreadPoolExecutor

import requests

from src.database import create_collections
from src.parsers.items_parser import parse_item
from src.threading_utils import max_workers


def save_download(url, downloads_collection):
    downloads_collection.insert_one({"url": url, "last_download_date": datetime.datetime.now()})


def save_item(item, items_collection):
    items_collection.insert_one(item)


def parse_and_save_items(successful_requests, items_collection, downloads_collection, mapping_collection):
    unparseable_items = []
    for successful_request in successful_requests:
        article, url = successful_request
        item = parse_item(article, mapping_collection)
        if isinstance(item, dict):
            save_download(url, downloads_collection)
            save_item(item, items_collection)
        else:
            unparseable_items.append(item)
    return unparseable_items


def fetch_and_save_items(articles, database):
    items_collection, mapping_collection, downloads_collection = create_collections(database)
    print(f'Starting data fetching process. Items to fetch: {len(articles)}')

    filtered = filter_already_downloaded_items(articles, downloads_collection)
    print(f'{len(articles) - len(filtered)} items have already been downloaded, skipping. New items to download: {len(filtered)}')

    with ThreadPoolExecutor(max_workers=max_workers()) as pool:
        fetch_results = pool.map(try_fetch, filtered)

    failed_requests, successful_requests = group_results(fetch_results)
    unparseable_items = parse_and_save_items(successful_requests, items_collection, downloads_collection, mapping_collection)

    failures = failed_requests + unparseable_items
    print(f'Finished data fetching process. Failures: {len(failures)}')
    print(failures)


def filter_already_downloaded_items(urls, downloads_collection):
    return [url for url in urls if not is_already_downloaded(url, downloads_collection)]


def is_already_downloaded(url, downloads_collection):
    return downloads_collection.find_one({"url": url}) is not None


def try_fetch(url):
    try:
        return requests.get(url, timeout=10), url
    except Exception as e:
        return e, url


def group_results(fetch_results):
    failed = []
    successful = []

    for result, url in fetch_results:
        if isinstance(result, Exception) or not result.ok:
            failed.append((result, url))
        else:
            successful.append((result, url))

    return failed, successful
