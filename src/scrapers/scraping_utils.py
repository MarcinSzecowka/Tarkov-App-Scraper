import datetime

import requests


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


def save_download(url, download_type, downloads_collection):
    downloads_collection.insert_one({
        "url": url,
        "type": download_type,
        "last_download_date": datetime.datetime.now()
    })