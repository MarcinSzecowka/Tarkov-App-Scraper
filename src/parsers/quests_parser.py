def append_quests(item, soup):
    all_h2_elements = soup.find_all("h2")
    for h2 in all_h2_elements:
        children = h2.find_all("span")
        for child in children:
            if child.getText() == "Quests":
                item["quests"] = []
                quests_element = h2.find_next_sibling()
                quests = quests_element.find_all("li")
                for quest in quests:
                    quest_dict = {}
                    quest_dict["trader"] = "Prapor"
                    all_quest_hrefs = quest.find_all("a", href=True)
                    if all_quest_hrefs[0]["href"] == "/wiki/Found_in_raid":
                        quest_dict["name"] = all_quest_hrefs[1].getText()
                        quest_dict["foundInRaidRequired"] = True
                    else:
                        quest_dict["name"] = all_quest_hrefs[0].getText()
                        quest_dict["foundInRaidRequired"] = False
                    try:
                        # quest_dict["itemCount"] = int(quest.getText().split(" ", 0)[0])
                        quest_dict["itemCount"] = int(quest.getText().split(" ", 1)[0])
                    except ValueError:
                        pass
                    item["quests"].append(quest_dict)
                else:
                    break