# data_loader.py

import requests
import random
from data_store import data_store

API_URL = "https://api.tarkov.dev/graphql"
HEADERS = {"Content-Type": "application/json"}


def _run_query(query, type_label):
    r = requests.post(API_URL, headers=HEADERS, json={"query": query})
    r.raise_for_status()
    counter = 0
    counter += 1

    items = r.json()["data"]["items"]

    out = []
    for item in items:
        out.append([
            type_label,
            item.get("name"),
            item.get("inspectImageLink"),
            item.get("types"),
            item.get("blocksHeadphones", False)
        ])
    return out


def preload_kit_data():
    print("[data_loader] Preloading kit data...")

    data_store.helmets = _run_query(
        """query { items(name: "Helmet", types: [wearable]) {
            name inspectImageLink blocksHeadphones types
        }}""",
        "Helmet"
    )

    data_store.headsets = _run_query(
        """query { items(name: "Headset", types: wearable) {
            name inspectImageLink
        }}""",
        "Headset"
    )

    data_store.masks = _run_query(
        """query { items(name: "Mask", types: wearable, gameMode: pve) {
            name inspectImageLink blocksHeadphones
        }}""",
        "Mask"
    )

    data_store.chest_rigs = _run_query(
        """query { items(type: rig, types: wearable) {
            name inspectImageLink types
        }}""",
        "Chest Rig"
    )

    data_store.armors = _run_query(
        """query { items(name: "Armor", types: armor) {
            name inspectImageLink types
        }}""",
        "Armor"
    )

    data_store.backpacks = _run_query(
        """query { items(name: "Backpack") {
            name inspectImageLink
        }}""",
        "Backpack"
    )

    data_store.grenades = _run_query(
        """query { items(types: grenade) {
            name inspectImageLink
        }}""",
        "Grenades"
    )

    data_store.guns = _run_query(
        """query { items(types: gun, type: wearable) {
            name inspectImageLink
        }}""",
        "Weapon"
    )

    print("[data_loader] Kit data loaded.")
