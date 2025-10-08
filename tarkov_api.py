import requests
from pprint import pprint 
import tarkov_api as api
import random

def kit_generator():
    # parse each response into a more formatted list
    # select a random index from the new list of items
    
    helmet_query = """query Helmets {items(name: "Helmet", types: helmet) {name iconLink}}"""
    helmet = requester(helmet_query, "Helmet")
    # print(f"Helmet: {helmet}")
    
    masks_query = """query Items {items(name: "Mask", types: wearable) {name iconLink}}"""
    mask = requester(masks_query, "Mask")
    # print(f"Mask: {mask}")

    headset_query = """query Items {items(name: "Headset", types: wearable) {name iconLink}}"""
    headset = requester(headset_query, "Headset")
    # print(f"Headset: {headset}")
    
    armor_query = """query Armor {items(name: "Armor", types: armor) {name iconLink}}"""
    armor = requester(armor_query, "Armor")
    # print(f"Armor: {armor}")

    backpack_query = """query Gear {items(name: "Backpack") {name iconLink}}"""
    backpack = requester(backpack_query, "Backpack")
    # print(f"Backpack: {backpack}")
    
    gun_query = """query Weapon {items(types: gun) {name iconLink}}"""
    gun = requester(gun_query, "Weapon")
    # print(f"Weapon: {gun}")
    
    yes_no = ["Yes", "No"]
    customized_weapon = random.choice(yes_no)
    # print(f"Customized Weapon: {customized_weapon}")

    grenade_query = """query Weapon {items(types: grenade) {name iconLink}}"""
    grenades = requester(grenade_query, "Grenades")
    # print(f"Grenades: {grenades}")

    # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
    # print(f"customized_weapon: {customized_weapon}")
    return helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon


def requester(query, type):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        list_of_items = [(item['name'], item['iconLink']) for item in response['data']['items']]
        string_with_empty = ("empty", "")
        list_of_items.append(string_with_empty)
        # print(list_of_items)
        random_string = random.choice(list_of_items)
        # print(random_string, type)
        return random_string, type
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

# if __name__ == "__main__":
#     kit_generator()