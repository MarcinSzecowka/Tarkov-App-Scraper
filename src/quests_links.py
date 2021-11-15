import requests

from src.article_utils import remove_none_types, append_protocol_and_domain
from src.items_links import WIKI_LINK
from src.parsers.item.category_parsers import quests_list_parser

QUESTS = '/wiki/Quests'


def fetch_all_quests_links():
    quests_link = WIKI_LINK + QUESTS
    quests = fetch_quest_links(quests_link, quests_list_parser)
    quests = remove_none_types(quests)
    quests = append_protocol_and_domain(quests)
    return quests


def fetch_quest_links(quests_link, parser):
    html = requests.get(quests_link)
    return parser(html)
