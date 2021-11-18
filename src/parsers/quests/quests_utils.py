from src.database import get_collections


def add_quests_ids_to_prev_and_next_fields(database):
    _, _, _, quests_collection = get_collections(database)
    enriched_quests = []
    quests = list(quests_collection.find())
    quests_by_name = {quest.get("name"): quest for quest in quests}
    for quest in quests:
        enriched_quest = dict(quest)
        enriched_quest["next"] = []
        enriched_quest["prev"] = []
        for next_quest_name in quest.get("next"):
            enriched_quest["next"].append(convert_to_dict_and_append_id(next_quest_name, quests_by_name))
        for prev_quest_name in quest.get("prev"):
            enriched_quest["prev"].append(convert_to_dict_and_append_id(prev_quest_name, quests_by_name))
        enriched_quests.append(enriched_quest)
    quests_collection.delete_many({})
    if enriched_quests:
        quests_collection.insert_many(enriched_quests)
    else:
        print("Enriched quests collection is empty, aborting")


def convert_to_dict_and_append_id(quest_name, quests_by_name):
    quest_lookup = quests_by_name.get(quest_name)
    enriched_quest_dict = {
        "_id": quest_lookup.get("_id") if quest_lookup else None,
        "name": quest_name
    }
    return enriched_quest_dict


def add_item_ids_to_quest_rewards(database):
    pass
