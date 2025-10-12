import requests
from pprint import pprint 
import assets.tarkov_api as api
import random

def image_by_name(body):
    list = body
    name = list[1]
    get_default_variant_query = """query Weapon {itemsByName(name: """ + f'"{name}"' + """) {name inspectImageLink}}"""  
    default_variant = default_variant_requester(get_default_variant_query)
    default_variant.insert(0, "Gun")
    return default_variant

def kit_generator():
    # parse each response into a more formatted list
    # select a random index from the new list of items
    blocking = False

    helmet_query = """query Helmets {items(name: "Helmet") {name inspectImageLink blocksHeadphones types}}"""
    helmet = requester(helmet_query, 'Helmet')
    # print(f"Helmet: {helmet}")
    if helmet[1] == True:
        helmet = [helmet[0], helmet[2], helmet[3]]
        headset = ['Headset', 'Empty', '']
        mask = ['Mask', 'Empty', '']
        
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")

        armor_query = """query Armor {items(name: "Armor", types: armor) {name inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        # print(f"Armor: {armor}")

        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")
        # print(f"Backpack: {backpack}")
        
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        # print(gun)
        
        # print(f"Weapon: {gun}")
        
        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        # print(f"Customized Weapon: {customized_weapon}")

        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(f"Grenades: {grenades}")

        # print(helmet, rig, armor, backpack, grenades, gun, customized_weapon)
        return helmet, rig, armor, backpack, grenades, gun, customized_weapon
    else:        
        helmet = [helmet[0], helmet[2], helmet[3]]
        masks_query = """query Items {items(name: "Mask", types: wearable) {name inspectImageLink } fleaMarket {enabled}}"""
        mask = requester(masks_query, "Mask")
        # print(f"Mask: {mask}")

        headset_query = """query Items {items(name: "Headset", types: wearable) {name inspectImageLink}}"""
        headset = requester(headset_query, "Headset")
        # print(f"Headset: {headset}")
        
        
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")

        
        armor_query = """query MyQuery {items(type: rig, types: wearable) {name inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        # print(f"Armor: {armor}")

        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")
        # print(f"Backpack: {backpack}")
        
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        
        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        # print(f"Customized Weapon: {customized_weapon}")

        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(f"Grenades: {grenades}")

        # print(f"customized_weapon: {customized_weapon}")

        # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
        return helmet, headset, mask, rig, armor, backpack, grenades, gun, customized_weapon
    
def requester(query, type):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        # print(response)
        if type == 'Helmet':
            helmets_with_type = [i for i in response['data']['items'] if 'glasses' not in i['types']]             
            # print(f"rigs_with_type : {rigs_with_type}")
            helmets = [list(d.values()) for d in helmets_with_type]
            list_of_helmets = []
            # Remove types: [glasses]
            for i in helmets:
                print(i)
                i.remove(i[3])
                i.insert(0, type)
                print(i)
                list_of_helmets.append(i)
            print(list_of_helmets)
            # list_of_items = [[type, item['blocksHeadphones'], item['name'], item['inspectImageLink']] for item in response['data']['items']]
            # list_of_items.append("empty")
            random_string = random.choice(list_of_items)
            return random_string
        else: 
            # print(type)
            if type == 'Chest Rig':
                rigs_with_type = [i for i in response['data']['items'] if 'armor' not in i['types']]             
                # print(f"rigs_with_type : {rigs_with_type}")
                rigs = [list(d.values()) for d in rigs_with_type]
                # print(rigs)
                list_of_rigs = []
                for i in rigs:
                    i.remove(i[1])
                    i.insert(0, type)
                    # print(i)
                    list_of_rigs.append(i)
                # print(list_of_rigs)
                
                final_rig = random.choice(list_of_rigs)
                # print(final_rig)
                return final_rig
            else: 
                list_of_items = [[type, item['name'], item['inspectImageLink']] for item in response['data']['items']]
                # print(list_of_items)
                # list_of_items.append("empty")
                random_string = random.choice(list_of_items)
                # print(random_string, type)
                return random_string
    
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def default_variant_requester(query):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        # print(response)
        # print('')
        list_of_items = [[item['name'], item['inspectImageLink']] for item in response['data']['itemsByName']]
        # print(f"list_of_items: {list_of_items}")
        for i in list_of_items:
            names = i[0]
            image = i[1]
            # print(names)            
            if check_last_word(names, "Default"):
                name_and_image = [names, image]
                return name_and_image
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def check_last_word(main_string, target_word):
    # Split the string by spaces and get the last element
    words = main_string.split()
    if not words:  # Handle empty strings
        return False
    last_word = words[-1]

    # Compare the last word with the target word
    return last_word == target_word

# if __name__ == "__main__":
#     kit_generator()