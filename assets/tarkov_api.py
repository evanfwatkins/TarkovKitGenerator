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
    
    helmet_query = """query Helmets {items(name: "Helmet" types: [wearable]) {name inspectImageLink blocksHeadphones types}}"""
    helmet = requester(helmet_query, 'Helmet')

    if helmet[3] == True:
        blocking_helmet = [helmet[0], helmet[1], helmet[2]]
        headset = ['Headset', 'Empty', '']
        mask = ['Mask', 'Empty', '']
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")
        armor_query = """query Armor {items(name: "Armor", types: armor) {name types inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(f"grenades: {grenades}")

        # print(helmet, rig, armor, backpack, grenades, gun, customized_weapon)
        return blocking_helmet, headset, mask, rig, armor, backpack, grenades, gun, customized_weapon
    else:        
        helmet = [helmet[0], helmet[1], helmet[2]]
        masks_query = """query Items {items(name: "Mask", types: wearable) {name inspectImageLink } fleaMarket {enabled}}"""
        mask = requester(masks_query, "Mask")
        headset_query = """query Items {items(name: "Headset", types: wearable) {name inspectImageLink}}"""
        headset = requester(headset_query, "Headset")        
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")        
        armor_query = """query MyQuery {items(type: rig, types: armor) {name inspectImageLink}}"""
        armor = requester(armor_query, "Armor")
        backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
        backpack = requester(backpack_query, "Backpack")        
        gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
        base_gun = requester(gun_query, "Weapon")
        gun = image_by_name(base_gun)
        yes_no = ["Yes", "No"]
        customized_weapon = random.choice(yes_no)
        
        grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
        grenades = requester(grenade_query, "Grenades")
        # print(grenades)


        # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
        return helmet, headset, mask, rig, armor, backpack, grenades, gun, customized_weapon
    
def requester(query, type):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        if type == 'Helmet':
            helmets_with_type = [i for i in response['data']['items'] if 'glasses' not in i['types']]             
            helmets = [list(d.values()) for d in helmets_with_type]
            list_of_helmets = []
            for i in helmets:
                i.remove(i[3])
                i.insert(0, type)
                list_of_helmets.append(i)
            random_string = random.choice(list_of_helmets)
            return random_string
        else: 
            if type == 'Armor':
                list_of_armor = []
                for i in response['data']['items']:
                    i = list(i.values())
                    i.insert(0, type)
                    list_of_armor.append(i)
                armor = random.choice(list_of_armor)
                return armor
            if type == 'Chest Rig':
                rigs_with_type = [i for i in response['data']['items'] if 'armor' not in i['types']]             
                rigs = [list(d.values()) for d in rigs_with_type]
                list_of_rigs = []
                for i in rigs:
                    i.remove(i[1])
                    i.insert(0, type)
                    list_of_rigs.append(i)
                
                final_rig = random.choice(list_of_rigs)
                return final_rig
            else: 
                list_of_items = [[type, item['name'], item['inspectImageLink']] for item in response['data']['items']]
                random_string = random.choice(list_of_items)
                return random_string
    
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def default_variant_requester(query):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        list_of_items = [[item['name'], item['inspectImageLink']] for item in response['data']['itemsByName']]
        for i in list_of_items:
            names = i[0]
            image = i[1]
            if check_last_word(names, "Default"):
                name_and_image = [names, image]
                return name_and_image
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def check_last_word(main_string, target_word):
    words = main_string.split()
    if not words:
        return False
    last_word = words[-1]

    return last_word == target_word

# if __name__ == "__main__":
#     kit_generator()