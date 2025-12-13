

import requests
from pprint import pprint
from pages import tarkov_api as api
import pages.tarkov_api as api
import random
import math
from data_store import data_store


def _pick(pool, fallback_label):
    if not pool:
        return [fallback_label, "Empty", f"/assets/images/empty_{fallback_label.lower()}_image.png"]
    return random.choice(pool)

def kit_generator():
    wears_mask = random.choice([True, False])
    list_of_blocking_masks = ['a','b','c']

    if wears_mask:
        helmet = ["Helmet", "Empty", "/assets/images/empty_helmet_image.png"]
        mask = _pick(data_store.masks, "Mask")
        if  mask[1] not in list_of_blocking_masks:
            headset = _pick(data_store.headsets, "Headset")
        else:
            headset
    else:
        helmet = _pick(data_store.helmets, "Helmet")
        if helmet[4]:  # blocksHeadphones
            headset = ["Headset", "Empty", "/assets/images/empty_headset_image.png"]
        else:
            headset = _pick(data_store.headsets, "Headset")
        mask = ["Mask", "Empty", "/assets/images/empty_mask_image.png"]

    rig = _pick(data_store.chest_rigs, "Chest Rig")
    
    if "plate carrier" or "armored rig" in rig[1]:
        armor = ['Armor', 'Empty', '/assets/images/empty_armor_image.png']
    else: 
        armor = _pick(data_store.armors,"Armor")
        
    backpack = _pick(data_store.backpacks, "Backpack")

    grenade_count = random.randint(1, 4)
    grenades = _pick(data_store.grenades, "Grenades")
    grenades[1] = f"{grenades[1]} x{grenade_count}"
    
    base_gun = _pick(data_store.guns, "Weapon")
    gun = image_by_name(base_gun, "Weapon")
    last_word = "Default"
    if check_last_word(gun[1], last_word):
        gun[1] = gun[1].replace(last_word, "").strip()

    customized_weapon = random.choice(["Yes", "No"])

    return (
        helmet,
        headset,
        mask,
        rig,
        armor,
        backpack,
        grenades,
        gun,
        customized_weapon
    )

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
            if type == 'Mask':
                masks_dict = [i for i in response['data']['items']]
                masks = [list(m.values()) for m in masks_dict]
                list_of_masks = []
                for i in masks:
                    i.insert(0, type)
                    list_of_masks.append(i)
                random_string = random.choice(list_of_masks)
                return random_string
            if type == 'Chest Rig':
                rigs_with_type = [i for i in response['data']['items']]             
                rigs = [list(d.values()) for d in rigs_with_type]
                list_of_rigs = []
                for i in rigs:
                    specs = i[1]
                    i.remove(i[1])
                    i.insert(0, type)
                    i.insert(3, specs)
                    list_of_rigs.append(i)                
                final_rig = random.choice(list_of_rigs)
                return final_rig
            if type == 'Armor':
                list_of_armor = []
                for i in response['data']['items']:
                    i = list(i.values())
                    types = i[1]
                    i.remove(i[1])
                    i.insert(0, type)
                    i.insert(3, types)
                    list_of_armor.append(i)
                armor = random.choice(list_of_armor)
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
    if type == "Weapon":
        get_default_variant_query = """query Weapon {itemsByName(name: """ + f'"{name}"' + """) {name inspectImageLink}}"""
        default_variant = default_variant_requester(get_default_variant_query)
        default_variant.insert(0, "Weapon")
        return default_variant
    if type == "Helmet":
        get_default_helmet_variant_query = """query Helmet {itemsByName(name: """ + f'"{name}"' + """) {name inspectImageLink}}"""
        default_helmet_variant = default_variant_requester(get_default_helmet_variant_query)
        default_helmet_variant.insert(0, "Helmet")
        return default_helmet_variant  
    else:
        print(f"Error with: {list}")

def default_variant_requester(query):
    headers = {"Content-Type": "application/json"}
    data = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if data.status_code == 200:
        response = data.json()
        names_list = [list(m.values()) for m in response["data"]["itemsByName"]]
        response_count = len(names_list)

        if response_count > 1:
            # Try to find a "Default" variant
            default_item = next((i for i in names_list if "Default" in i[0]), None)
            name_and_image = default_item if default_item else names_list[0]
            return name_and_image
        else:
            name_and_image = names_list[0]
            return name_and_image
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(data.status_code, query))

def check_last_word(main_string, target_word):
    words = main_string.split()
    if not words:
        return False
    last_word = words[-1]

    return last_word == target_word

def weapon_customizer(gun_name):   
    # magazine_query = ["Yes", "No"]
    # magazine  = ["Magazine", random.choice(magazine_query)]
    # print(f"magazine: {magazine}")

    suppressor_query = ["Yes", "No"]
    suppresor = ["Suppressor", random.choice(suppressor_query)]
    # print(f"suppresor: {suppresor}")

    foregrip_query = ["Yes", "No"]
    foregrip = ["Foregrip", random.choice(foregrip_query)]
    # print(f"foregrip: {foregrip}")

    optic_query = ["Yes", "No"]
    optic = ["Optic", random.choice(optic_query)]
    # print(f"optic: {optic}")

    flashlight_query = ["Yes", "No"]
    flashlight = ["Flashlight", random.choice(flashlight_query)]
    # print(f"flashlight: {flashlight}")

    # print(magazine, suppresor, foregrip, optic, flashlight)
    return suppresor, foregrip, optic, flashlight

# hideout stations - query MyQuery {hideoutStations(gameMode: pve) {name}}
# All stations upgrades - query MyQuery {hideoutStations(gameMode: pve) {name levels {itemRequirements {item {name inspectImageLink} count}}}}

def get_hideout_upgrades(query, station):
    headers = {"Content-Type": "application/json"}
    data = requests.post(
        "https://api.tarkov.dev/graphql",
        headers=headers,
        json={"query": query},
    )

    if data.status_code != 200:
        return []

    response = data.json()

    # Find matching station
    station_data = next(
        (
            s for s in response["data"]["hideoutStations"]
            if s["name"] == station
        ),
        None,
    )

    if not station_data:
        return []

    levels_out = []

    for idx, level in enumerate(station_data["levels"], start=1):
        requirements = []

        for req in level["itemRequirements"]:
            requirements.append(
                (
                    req["item"]["name"],
                    req["count"],
                    req["item"]["inspectImageLink"],

                )
            )

        levels_out.append(
            {
                "level": idx,
                "requirements": requirements,
            }
        )

    return levels_out

def get_hideout_crafts(query, station):
    headers = {"Content-Type": "application/json"}
    res = requests.post(
        "https://api.tarkov.dev/graphql",
        headers=headers,
        json={"query": query},
    )

    if res.status_code != 200:
        return []

    data = res.json()["data"]["hideoutStations"]
    
    station_data = next(
        (s for s in data if s["name"] == station),
        None,
    )

    if not station_data or not station_data["crafts"]:
        return []

    crafts_out = []

    for craft in station_data["crafts"]:
        requirements = [
            (
                req["item"]["name"],
                req["count"],
                req["item"]["inspectImageLink"],
            )
            for req in craft["requiredItems"]
        ]
        

        outputs = [
            (
                out["item"]["name"],
                out.get("count", 1),
                out["item"]["inspectImageLink"],
            )
            for out in craft["rewardItems"]
        ]

        crafts_out.append(
            {
                "level": craft["level"],
                "duration": craft["duration"],
                "requirements": requirements,
                "outputs": outputs,
            }
        )
    return crafts_out

if __name__ == "__main__":
    kit_generator()