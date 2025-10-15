import requests
from pprint import pprint 
import assets.tarkov_api as api
import random

def kit_generator():    
    helmet_query = """query Helmets {items(name: "Helmet" types: [wearable]) {name inspectImageLink blocksHeadphones types}}"""
    helmet = requester(helmet_query, 'Helmet')
    # print(helmet)
    # print(helmet[3])
    if helmet[3] == True:
        base_helmet = helmet
        blocking_helmet = image_by_name(base_helmet, "Helmet")
        # print(f"blocking_helmet: {blocking_helmet}")
        blocking_helmet = ["Helmet", blocking_helmet[1], blocking_helmet[2]]
        headset = ['Headset', 'Empty', '/assets/images/empty_headset_image.png']
        mask = ['Mask', 'Empty', '/assets/images/empty_mask_image.png']
        rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
        rig = requester(rig_query, "Chest Rig")
        print(rig)
        if "plate carrier" in rig[1]:
            armor = ['Armor', 'Empty', '/assets/images/empty_armor_image.png']
            backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
            backpack = requester(backpack_query, "Backpack")
            gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
            base_gun = requester(gun_query, "Weapon")
            gun = image_by_name(base_gun, "Weapon")
            yes_no = ["Yes", "No"]
            customized_weapon = random.choice(yes_no)
            grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
            grenades = requester(grenade_query, "Grenades")
        else: 
            armor_query = """query Armor {items(name: "Armor", types: armor) {name types inspectImageLink}}"""
            armor = requester(armor_query, "Armor")
            backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
            backpack = requester(backpack_query, "Backpack")
            gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
            base_gun = requester(gun_query, "Weapon")
            gun = image_by_name(base_gun, "Weapon")
            yes_no = ["Yes", "No"]
            customized_weapon = random.choice(yes_no)
            grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
            grenades = requester(grenade_query, "Grenades")

        return blocking_helmet, headset, mask, rig, armor, backpack, grenades, gun, customized_weapon
    else:        
        if "SLAAP" in helmet[1]:
            helmet = ['Helmet', 'Empty', '/assets/images/empty_helmet_image.png']
        else: 
            helmet = helmet
            masks_query = """query Items {items(name: "Mask", types: wearable, gameMode: pve) {name blocksHeadphones inspectImageLink}}"""
            mask = requester(masks_query, "Mask")
            if mask[2] == True:
                mask = [mask[0], mask[1], mask[3]] 
                headset_query = ['Headset', 'Empty', '/assets/images/empty_headset_image.png']
                headset = requester(headset_query, "Headset")        
                rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
                rig = requester(rig_query, "Chest Rig")        
                if "plate carrier" in rig[1]:
                    print("BALLS")
                    armor = ['Armor', 'Empty', '/assets/images/empty_armor_image.png']
                    backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
                    backpack = requester(backpack_query, "Backpack")
                    gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
                    base_gun = requester(gun_query, "Weapon")
                    gun = image_by_name(base_gun, "Weapon")
                    yes_no = ["Yes", "No"]
                    customized_weapon = random.choice(yes_no)
                    grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
                    grenades = requester(grenade_query, "Grenades")
                    # print(f"grenades: {grenades}")
                else: 
                    armor_query = """query Armor {items(name: "Armor", types: armor) {name types inspectImageLink}}"""
                    armor = requester(armor_query, "Armor")
                    backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
                    backpack = requester(backpack_query, "Backpack")
                    gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
                    base_gun = requester(gun_query, "Weapon")
                    gun = image_by_name(base_gun, "Weapon")
                    yes_no = ["Yes", "No"]
                    customized_weapon = random.choice(yes_no)
                    grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
                    grenades = requester(grenade_query, "Grenades")
                    # print(f"grenades: {grenades}")

                # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
                return helmet, mask, headset, rig, armor, backpack, grenades, gun, customized_weapon
            else:
                mask = [mask[0], mask[1], mask[3]] 
                headset_query = """query Items {items(name: "Headset", types: wearable) {name inspectImageLink}}"""
                headset = requester(headset_query, "Headset")        
                rig_query = """query MyQuery {items(type: rig, types: wearable) {name types inspectImageLink}}"""
                rig = requester(rig_query, "Chest Rig")        
                armor_query = """query Armor {items(name: "Armor", types: armor) {name types inspectImageLink}}"""
                armor = requester(armor_query, "Armor")
                backpack_query = """query Gear {items(name: "Backpack") {name inspectImageLink}}"""
                backpack = requester(backpack_query, "Backpack")        
                gun_query = """query Weapon {items(types: gun, type: wearable) {name inspectImageLink}}"""
                base_gun = requester(gun_query, "Weapon")
                gun = image_by_name(base_gun, "Weapon")
                yes_no = ["Yes", "No"]
                customized_weapon = random.choice(yes_no)
                
                grenade_query = """query Weapon {items(types: grenade) {name inspectImageLink}}"""
                grenades = requester(grenade_query, "Grenades")
                # print(grenades)

                # print(helmet, headset, mask, armor, backpack, grenades, gun, customized_weapon)
                return helmet, mask, headset, rig, armor, backpack, grenades, gun, customized_weapon

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
            # print(random_string)
            return random_string
        else: 
            if type == 'Mask':
                masks_dict = [i for i in response['data']['items']]
                masks = [list(m.values()) for m in masks_dict]
                list_of_masks = []
                for i in masks:
                    i.insert(0, type)
                    list_of_masks.append(i)
                random_string = random.choice(list_of_masks)
                # print(f"mask random_string: {random_string}")
                return random_string
            if type == 'Chest Rig':
                rigs_with_type = [i for i in response['data']['items'] if 'armor' or 'rig' not in i['types']]             
                rigs = [list(d.values()) for d in rigs_with_type]
                list_of_rigs = []
                for i in rigs:
                    i.remove(i[1])
                    i.insert(0, type)
                    list_of_rigs.append(i)                
                final_rig = random.choice(list_of_rigs)
                # print(f"final_rig: {final_rig}")
                return final_rig
            if type == 'Armor':
                list_of_armor = []
                for i in response['data']['items']:
                    i = list(i.values())
                    i.insert(0, type)
                    del i[2]
                    # print(f"i: {i}")
                    list_of_armor.append(i)
                armor = random.choice(list_of_armor)
                # print(f"armor: {armor}")
                return armor
            else: 
                list_of_items = [[type, item['name'], item['inspectImageLink']] for item in response['data']['items']]
                random_string = random.choice(list_of_items)
                return random_string
    
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(data.status_code, query))

def image_by_name(body, type):
    list = body
    name = list[1]
    # print(f"list: {list}")
    # print(f"name: {name}", f"type: {type}")
    if type == "Weapon":
        get_default_variant_query = """query Weapon {itemsByName(name: """ + f'"{name}"' + """) {name inspectImageLink}}"""
        default_variant = default_variant_requester(get_default_variant_query)
        default_variant.insert(0, "Weapon")
        return default_variant
    if type == "Helmet":
        # print(list)
        # print(name)
        get_default_helmet_variant_query = """query Helmet {itemsByName(name: """ + f'"{name}"' + """) {name inspectImageLink}}"""
        # print(get_default_helmet_variant_query)
        default_helmet_variant = default_variant_requester(get_default_helmet_variant_query)
        default_helmet_variant.insert(0, "Helmet")
        # print(f"default_helmet_variant: {default_helmet_variant}")
        # print(default_helmet_variant)
        return default_helmet_variant  
    else:
        print(f"Error with: {list}")

def default_variant_requester(query):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        # print(response)
        names_list = [list(m.values()) for m in response["data"]["itemsByName"]]

        # print(f"list_of_names: {names_list}")
        response_count = len(names_list)

        if response_count > 1:
            # Try to find a "Default" variant
            default_item = next((i for i in names_list if "Default" in i[0]), None)
            name_and_image = default_item if default_item else names_list[0]
            # print(f"name_and_image: {name_and_image}")
            return name_and_image
        else:
            name_and_image = names_list[0]
            # print(name_and_image)
            return name_and_image
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(data.status_code, query))

def check_last_word(main_string, target_word):
    words = main_string.split()
    # print(words)
    if not words:
        return False
    last_word = words[-1]

    return last_word == target_word

# if __name__ == "__main__":
#     kit_generator()