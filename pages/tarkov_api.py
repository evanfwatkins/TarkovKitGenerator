

import random
import requests
from data_store import data_store


EMPTY_IMAGES = {
    "Helmet": "/assets/images/empty_helmet_image.png",
    "Headset": "/assets/images/empty_headset_image.png",
    "Mask": "/assets/images/empty_mask_image.png",
    "Armor": "/assets/images/empty_armor_image.png",
}


def _select_item(pool, slot):
    if not pool:
        return {
            "slot": slot,
            "name": "Unavailable",
            "image": EMPTY_IMAGES.get(slot),
            "types": [],
            "blocksHeadphones": False,
        }

    item = random.choice(pool)
    return {
        "slot": slot,
        "name": item["name"],
        "image": item.get("inspectImageLink") or EMPTY_IMAGES[slot],
        "types": item.get("types", []),
        "blocksHeadphones": bool(item.get("blocksHeadphones", False)),
    }


def kit_generator():
    wears_mask = random.choice([True, False])
    helmet = _select_item(data_store.helmets, "Helmet")
    mask = _select_item(data_store.masks, "Mask")
    if wears_mask:
        helmet = _select_item([], "Helmet")
    else:
        mask = _select_item([], "Mask")

    headset = _select_item(data_store.headsets, "Headset")
    if helmet["blocksHeadphones"] or (wears_mask and headset["blocksHeadphones"]):
        headset = _select_item([], "Headset")

    rig = _select_item(data_store.chest_rigs, "Chest Rig")
    armor = (
        _select_item([], "Armor")
        if "armor" in rig["types"]
        else _select_item(data_store.armors, "Armor")
    )
    backpack = _select_item(data_store.backpacks, "Backpack")
    grenades = _select_item(data_store.grenades, "Grenades")
    grenades["name"] = f"{grenades['name']} x{random.randint(1, 4)}"
    gun = _select_item(data_store.guns, "Weapon")

    customized_weapon = random.choices(["Yes", "No"], weights=[80, 20], k=1)[0]
    return [helmet, headset, mask, rig, armor, backpack, grenades, gun], customized_weapon

def weapon_customizer(gun_name):
    # magazine_query = ["Yes", "No"]
    # magazine  = ["Magazine", random.choice(magazine_query)]
    # print(f"magazine: {magazine}")

    
    suppressor_query = ["Yes", "No"]
    suppresor = ["Suppressor", random.choices(suppressor_query, weights=[60, 40], k=1)[0]]
    # print(f"suppresor: {suppresor}")

    foregrip_query = ["Yes", "No"]

    if "pistol" in gun_name.lower() or "mosin" in gun_name.lower():
        foregrip = ["Foregrip", "No"]
    else:
        foregrip = ["Foregrip", random.choices(foregrip_query, weights=[60, 40], k=1)[0]]
    # print(f"foregrip: {foregrip}")
    
    optic_query = ["Yes", "No"]
    optic = ["Optic", random.choices(optic_query, weights=[60, 40], k=1)[0]]
    # print(f"optic: {optic}")

    flashlight_query = ["Yes", "No"]
    flashlight = ["Flashlight", random.choices(flashlight_query, weights=[60, 40], k=1)[0]]
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