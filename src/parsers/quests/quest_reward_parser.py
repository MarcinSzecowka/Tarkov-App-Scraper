import re

experience_re = re.compile(r"^\+[0-9,]* EXP$")
reputation_re = re.compile(r"^([a-zA-Z]*) Rep \+([0-9.]*)$")
money_re = re.compile(r"^([0-9,]*) (Roubles|Dollars|Euros)$")
item_re = re.compile("^([0-9]+)× (.*)$")


def parse_basic_reward(reward_list_item):
    return {
        "type": "basic_reward",
        "value": reward_list_item.getText().strip()
    }


def is_item_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    return item_re.match(text) is not None


def parse_item_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    match = item_re.match(text)
    return {
        "type": "item_reward",
        "item": match.group(2),
        "count": match.group(1)
    }


def is_money_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    return money_re.match(text) is not None


def parse_money_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    match = money_re.match(text)
    return {
        "type": "money_reward",
        "value": match.group(1),
        "currency": match.group(2)
    }


def is_reputation_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    return reputation_re.match(text) is not None


def parse_reputation_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    match = reputation_re.match(text)
    return {
        "type": "reputation_reward",
        "trader": match.group(1),
        "value": match.group(2)
    }


def is_experience_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    return experience_re.match(text) is not None


def parse_experience_reward(reward_list_item):
    text = reward_list_item.getText().strip()
    text = text.removeprefix("+")
    text = text.removesuffix(" EXP")
    amount = float(text.replace(",", ""))
    return {
        "type": "experience_reward",
        "value": amount
    }
