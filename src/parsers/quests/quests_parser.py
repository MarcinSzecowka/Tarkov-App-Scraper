from bs4 import BeautifulSoup

from src.parsers.general_data_table_parser import get_general_data, get_related_quests
from src.parsers.quests.quest_reward_parser import is_experience_reward, parse_experience_reward, is_reputation_reward, \
    parse_reputation_reward, is_money_reward, parse_money_reward, is_item_reward, parse_item_reward, parse_basic_reward
from src.utils import with_id

QUEST_DATA_LABEL = "Quest data"
GIVEN_BY_LABEL = "Given By"
REQUIRED_FOR_KAPPA_LABEL = "Required forKappa"
LOCATION_LABEL = "Location"


def parse_quest(article):
    quest = {}
    soup = BeautifulSoup(article.content, "lxml")
    append_general_data(quest, soup)
    append_requirements(quest, soup)
    append_objectives(quest, soup)
    append_rewards(quest, soup)
    return quest


def append_general_data(quest, soup):
    general_data = get_general_data(soup)
    quest["name"] = general_data.title
    quest_data = general_data.get_section(QUEST_DATA_LABEL)
    quest["given_by"] = quest_data.get_value(GIVEN_BY_LABEL)
    append_locations(quest, quest_data)
    required_for_kappa = quest_data.get_value(REQUIRED_FOR_KAPPA_LABEL)
    quest["required_for_kappa"] = required_for_kappa.strip().lower() == "yes"
    related_quests = get_related_quests(general_data)
    quest["prev"] = related_quests["prev"]
    quest["next"] = related_quests["next"]


def append_locations(quest, quest_data):
    location = quest_data.get_value(LOCATION_LABEL)
    if location:
        locations = location.strip().split(",")
        quest["location"] = [location_name.strip() for location_name in locations]


def append_requirements(quest, soup):
    requirements = []
    requirements_span = soup.find("span", with_id("Requirements"))
    if requirements_span:
        ul = requirements_span.find_parent().find_next_sibling("ul")
        if ul:
            list_items = ul.find_all("li")
            for list_item in list_items:
                requirements.append(list_item.getText())
    quest["requirements"] = requirements


def append_objectives(quest, soup):
    objectives = []
    objectives_span = soup.find("span", with_id("Objectives"))
    if objectives_span:
        ul = objectives_span.find_parent().find_next_sibling("ul")
        if ul:
            objectives_text_split = ul.getText().split("\n")
            for objective_text in objectives_text_split:
                is_optional = "(Optional)".lower() in objective_text.strip().lower()
                objective_dict = {
                    "description": objective_text.strip().removeprefix("(Optional)"),
                    "optional": is_optional
                }
                objectives.append(objective_dict)
    quest["objectives"] = objectives


def append_rewards(quest, soup):
    rewards = []
    rewards_span = soup.find("span", with_id("Rewards"))
    if rewards_span:
        ul = rewards_span.find_parent().find_next_sibling("ul")
        for reward_list_item in ul.find_all("li", recursive=False):
            rewards.append(parse_reward(reward_list_item))
    quest["rewards"] = rewards


def parse_reward(reward_list_item):
    if is_experience_reward(reward_list_item):
        reward = parse_experience_reward(reward_list_item)
    elif is_reputation_reward(reward_list_item):
        reward = parse_reputation_reward(reward_list_item)
    elif is_money_reward(reward_list_item):
        reward = parse_money_reward(reward_list_item)
    elif is_item_reward(reward_list_item):
        reward = parse_item_reward(reward_list_item)
    else:
        reward = parse_basic_reward(reward_list_item)

    return reward
