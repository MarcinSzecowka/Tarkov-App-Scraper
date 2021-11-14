WIKI_LINK = "https://escapefromtarkov.fandom.com"


def remove_none_types(articles):
    return [article for article in articles if article is not None]


def append_protocol_and_domain(articles):
    return [WIKI_LINK + article for article in articles if article]
