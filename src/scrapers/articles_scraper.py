from concurrent.futures import ThreadPoolExecutor

import requests

from src.utils import max_workers


def fetch_articles_from_given_category(category_and_parser):
    category, parser = category_and_parser
    html = requests.get(category)
    return html, parser


def fetch_remaining_articles(categories_and_parsers):
    articles = []
    with ThreadPoolExecutor(max_workers=max_workers()) as pool:
        res = pool.map(fetch_articles_from_given_category, categories_and_parsers)
    for html, parser in res:
        fetched_articles = parser(html)
        articles.extend(fetched_articles)
    return articles
