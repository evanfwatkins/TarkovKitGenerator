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
    
    helmet_query = """query Helmets {items(name: "Helmet") {name inspectImageLink blocksHeadphones types}}"""
    helmet = requester(helmet_query, 'Helmet')

    if helmet[2] == True:
        blocking_helmet = [helmet[0], helmet[1], helmet[2]]
        # print(f"blocking_helmet: {blocking_helmet}")
 
        headset = ['Headset', 'Empty', '']
        # print(f"headset: {headset}")

        mask = ['Mask', 'Empty', '']
        # print(f"mask: {mask}")
        
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")
        # print(f"rig: {rig}")

        armor_query = """query Armor {items(name: "Armor", types: armor) {name types inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        # print(f"armor: {armor}")

        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")
        # print(f"backpack: {backpack}")
        
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        # print(f"gun: {gun}")
        
        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        # print(f"Customized Weapon: {customized_weapon}")

        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(f"grenades: {grenades}")

        # print(helmet, rig, armor, backpack, grenades, gun, customized_weapon)
        return blocking_helmet, rig, armor, backpack, grenades, gun, customized_weapon
    else:        
        helmet = [helmet[0], helmet[1], helmet[2]]
        # print(helmet)

        masks_query = """query Items {items(name: "Mask", types: wearable) {name inspectImageLink } fleaMarket {enabled}}"""
        mask = requester(masks_query, "Mask")
        # print(mask)

        headset_query = """query Items {items(name: "Headset", types: wearable) {name inspectImageLink}}"""
        headset = requester(headset_query, "Headset")
        # print(headset)        
        
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")
        # print(rig)
        
        armor_query = """query MyQuery {items(type: rig, types: armor) {name inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        # print(armor)

        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")
        # print(backpack)
        
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        # print(gun)

        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        # print(f"Customized Weapon: {customized_weapon}")

        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(grenades)

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
            helmets = [list(d.values()) for d in helmets_with_type]
            # print(f'helmets>helmet list: {helmets}')
            list_of_helmets = []
            for i in helmets:
                # print(i)
                i.insert(0, type)
                i.remove(i[3])
                # print(i)
                list_of_helmets.append(i)
            random_string = random.choice(list_of_helmets)
            # print(random_string)
            return random_string
        else: 
            print(type)
            if type == 'Armor':
                print(response)
                armor_with_type = [i for i in response['data']['items'] if 'armor' in i['types']]
                print(f"armor_with_type: {armor_with_type}")
                armors = [list(d.values()) for d in armor_with_type]
                print(f"Armors: {armors}")
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