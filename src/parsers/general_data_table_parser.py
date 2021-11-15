from src.parsers.parser_utils import find_general_data_table
from src.utils import with_class


class GeneralData(object):
    def __init__(self, title=None):
        self.title = title
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def get_section(self, header_text):
        for section in self.sections:
            if header_text.strip().lower() in section.header.strip().lower():
                return section
        return None


class Section(object):
    def __init__(self, soup, header=None):
        self.soup = soup
        self.header = header
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def get_value(self, key):
        for row in self.rows:
            if key.strip().lower() in row.key.strip().lower():
                return row.value
        return None


class Row(object):
    def __init__(self, key, value, soup):
        self.key = key
        self.value = value
        self.soup = soup


def get_general_data(soup):
    general_data = GeneralData()

    table = find_general_data_table(soup)
    if table:
        general_data.title = get_title(table)
        sections = get_sections(table)
        for section in sections:
            general_data.add_section(section)

    return general_data


def get_sections(table):
    result = []

    table_sections = table.find_all("table", {"class": "va-infobox-group"})
    for table_section in table_sections:
        section = get_section(table_section)
        if section.header or section.rows:
            result.append(section)

    return result


def get_title(table):
    header = table.find("tr", {"class": "va-infobox-row-title"})
    return header.getText() if header else None


def get_section(table_section):
    header = table_section.find("th", {"class": "va-infobox-header"})
    section = Section(table_section, header=header.getText() if header else None)

    labels = table_section.find_all("td", {"class": "va-infobox-label"})
    for label in labels:
        content = label.find_next_sibling("td", with_class("va-infobox-content"))
        if content:
            row = Row(key=label.getText(), value=content.getText(), soup=content)
            section.add_row(row)

    return section


def get_related_quests(general_data):
    result = {
        "prev": [],
        "next": []
    }

    section = general_data.get_section("Related quests")
    if section:
        content = section.soup.find_all("td", with_class("va-infobox-content"))
        for td in content:
            if "Previous".lower() in td.getText().strip().lower():
                links = td.find_all("a")
                for link in links:
                    result["prev"].append(link.getText().strip())
            if "Leads to".lower() in td.getText().strip().lower():
                links = td.find_all("a")
                for link in links:
                    result["next"].append(link.getText().strip())

    return result



