def parse_hideout_module(table_header):
    hideout_module = {}
    link = table_header.find("a")
    if link:
        text = link.getText().strip().split("level")
        hideout_module["name"] = text[0].strip()
        hideout_module["level"] = text[1].strip()
    hideout_module["time"] = table_header.find("br").next.getText().strip()
    return hideout_module
