def find_general_data_table(soup):
    return soup.find("table", {"class": "va-infobox"})


def get_page_title(soup):
    return soup.find("h1", {"class": "page-header__title"}).getText()
