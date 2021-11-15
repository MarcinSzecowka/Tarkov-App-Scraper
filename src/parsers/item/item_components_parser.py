def parse_item_components(table_header, mapping_collection):
    components = []
    full_text = table_header.getText()
    links = find_all_links_without_children(table_header)
    for link in links:
        component = parse_item_component(link, full_text, mapping_collection)
        components.append(component)
    return components


def parse_item_component(link, full_text, mapping_collection):
    item_component = {}
    item_component_name = link.getText().strip()
    item_component["name"] = item_component_name
    item_component["count"] = parse_component_count(item_component_name, full_text)
    item_component["id"] = fetch_item_id_from_database(item_component_name, mapping_collection)
    return item_component


def find_all_links_without_children(table_header):
    links = table_header.find_all("a")
    return list(filter(lambda link: not link.find("img"), links))


def parse_component_count(item_component_name, full_text):
    split = full_text.strip().split("+")
    for word in split:
        if item_component_name in word:
            count_text = word.strip().removesuffix(item_component_name)
            if count_text == '':
                return str(1)
            return count_text.removeprefix("x").strip()
    return None


def parse_component_image(table_header, link):
    link_with_image = table_header.find("a", {"title": link.getText()})
    if link_with_image:
        image = link_with_image.find("img")
        if image:
            data_src = image.get("data-src")
            src = image.get("src")
            if data_src:
                return data_src
            elif src:
                return src
    return None


def fetch_item_id_from_database(item_component_name, mapping_collection):
    mapping = mapping_collection.find_one({"name": item_component_name})
    if mapping:
        return mapping["id"]
    return "undefined"
