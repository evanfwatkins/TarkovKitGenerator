import requests
from pprint import pprint 
import assets.tarkov_api as api
import random

def kit_generator():
    # parse each response into a more formatted list
    # select a random index from the new list of items
    blocking = False

    helmet_query = """query Helmets {items(name: "Helmet") {name iconLink blocksHeadphones}}"""
    helmet = requester(helmet_query, 'Helmet')
    print(f"Helmet: {helmet}")
    if helmet[1] == True:
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

        # print(helmet, headset,mask, armor, backpack, grenades, gun, customized_weapon)
        # print(f"customized_weapon: {customized_weapon}")

        return helmet, armor, backpack, grenades, gun, customized_weapon
    else:

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

        # print(f"customized_weapon: {customized_weapon}")
        # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
        return helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon
    
# return helmet 

def requester(query, type):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        # print(response)
        if type == 'Helmet':
            list_of_items = [[type, item['blocksHeadphones'], item['name'], item['iconLink']] for item in response['data']['items']]
            list_of_items.append("empty")
            # random_string = random.choice(list_of_items)
        else: 
            list_of_items = [[type, item['name'], item['iconLink']] for item in response['data']['items']]
            list_of_items.append("empty")
            random_string = random.choice(list_of_items)
            # print(random_string, type)
        return random_string
    
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

# if __name__ == "__main__":
#     kit_generator()