# pages/tarkov_api.py
"""
Replaces request-per-click logic with in-memory sampling from data_store.
Function signatures kept compatible with existing page usage:
- kit_generator()
- weapon_customizer(gun_name)
- get_hideout_upgrades(query, station)  # still accepts query param for compatibility
- get_hideout_crafts(query, station)
"""

import random
from data_store import data_store
import math

# ---------- Helpers ----------

def _get_items_df():
    return data_store.items_df if data_store.items_df is not None else None


def _sample_items_by_pred(pred, type_label):
    """
    pred: function(row_dict) -> bool
    returns an item list in the same light structure your pages expect:
      ['TypeLabel', name, inspectImageLink, ...optional fields...]
    """
    items = data_store.items_raw or []
    candidates = [i for i in items if pred(i)]
    if not candidates:
        # fallback placeholder (keeps UI safe)
        return [type_label, f"Empty {type_label}", f"/assets/images/empty_{type_label.lower()}_image.png"]
    sel = random.choice(candidates)
    name = sel.get("name", "Unknown")
    image = sel.get("inspectImageLink") or f"/assets/images/empty_{type_label.lower()}_image.png"
    # return at least three elements (index 0..2) as your UI uses [0]=header, [1]=name, [2]=image
    # put types or blocksHeadphones as index 3 if needed
    return [type_label, name, image, sel.get("types", None), sel.get("blocksHeadphones", False)]


# ---------- Kit generator ----------

def kit_generator():
    """
    Returns 9-tuple compatible with your existing code:
    (helmet, headset, mask, rig, armor, backpack, grenades, weapon, customized_weapon)
    Each element is a list like ['Helmet', name, image, ...]
    """
    # Helmet logic: find wearable items that look like helmets (heuristic)
    helmet = _sample_items_by_pred(lambda i: "wearable" in _types_lower(i) and "helmet" in i.get("name","").lower(), "Helmet")

    # Grenades
    # fallback: any item whose types contains 'grenade'
    grenade_quantity = random.randint(1, 4)
    grenades = [f"Grenades x{grenade_quantity}", "Multiple", "/assets/images/grenade_image.png"]

    # Mask
    mask = _sample_items_by_pred(lambda i: "wearable" in _types_lower(i) and "mask" in i.get("name","").lower(), "Mask")

    # Headset (if mask blocks headphones, show empty headset)
    # Use blocksHeadphones if present on helmet/mask; otherwise allow headset
    blocks = helmet[4] or mask[4]
    if blocks:
        headset = ['Headset', 'Empty', '/assets/images/empty_headset_image.png']
    else:
        headset = _sample_items_by_pred(lambda i: "wearable" in _types_lower(i) and "headset" in i.get("name","").lower(), "Headset")

    # Rig
    rig = _sample_items_by_pred(lambda i: "rig" in i.get("types", []) or "rig" in i.get("name","").lower(), "Chest Rig")

    # Armor: prefer armor types
    armor_candidate = _sample_items_by_pred(lambda i: any(t for t in _types_lower(i) if "armor" in t or "vest" in t or "carrier" in t), "Armor")
    # If rig implies plate carrier, sometimes armor is empty; but keep simple:
    armor = armor_candidate

    # Backpack
    backpack = _sample_items_by_pred(lambda i: "backpack" in i.get("name","").lower() or "backpack" in _types_lower(i), "Backpack")

    # Weapon: pick any item with types containing 'gun' or 'weapon'
    weapon = _sample_items_by_pred(lambda i: any("gun" in t or "weapon" in t for t in _types_lower(i)), "Weapon")
    weapon = weapon
    weapon = image_by_name(weapon, "Weapon")
    # Customized weapon yes/no
    customized_weapon = random.choice(["Yes", "No"])

    # Return same shape your UI expects
    return helmet, headset, mask, rig, armor, backpack, grenades, weapon, customized_weapon


def _types_lower(item):
    """Return types as list of lowercase strings for robust checks."""
    types = item.get("types", [])
    if isinstance(types, str):
        # if it's a comma-separated string
        return [t.strip().lower() for t in types.split(",")]
    if isinstance(types, (list, tuple)):
        return [str(t).lower() for t in types]
    return []

def image_by_name(body, type):
    """
    Fully in-memory replacement.
    Works identically to the old image_by_name(), but pulls the item
    from data_store.items_by_name or from a substring match.
    """
    if not body or len(body) < 2:
        return [type, "Unknown", f"/assets/images/empty_{type.lower()}_image.png"]

    name = body[1]
    return image_by_name_equivalent(name, type)



def image_by_name_equivalent(name, item_type="Weapon"):
    """
    If you previously called image_by_name_equivalent to lookup the default variant for a weapon/helmet,
    try to find the item by name in the cached store.
    Returns ['Weapon', name, image] style list.
    """
    print(name)
    if not name:
        return [item_type, "Unknown", f"/assets/images/empty_{item_type.lower()}_image.png"]
    item = data_store.items_by_name.get(name.lower())
    if item:
        return [item_type, item.get("name", name), item.get("inspectImageLink") or f"/assets/images/empty_{item_type.lower()}_image.png"]
    # fallback: best-effort search by substring
    items = data_store.items_raw or []
    match = next((i for i in items if name.lower() in i.get("name","").lower()), None)
    if match:
        return [item_type, match.get("name"), match.get("inspectImageLink")]
    return [item_type, name, f"/assets/images/empty_{item_type.lower()}_image.png"]


# ---------- Weapon customizer (kept same signature) ----------

def weapon_customizer(gun_name):
    """
    Return tuple of attachments:
    (suppressor, foregrip, optic, flashlight) each is ['Label', 'Yes'|'No']
    """
    suppressor = ["Suppressor", random.choice(["Yes", "No"])]
    foregrip = ["Foregrip", random.choice(["Yes", "No"])]
    optic = ["Optic", random.choice(["Yes", "No"])]
    flashlight = ["Flashlight", random.choice(["Yes", "No"])]
    return suppressor, foregrip, optic, flashlight


# ---------- Hideout (reads from cached hideout_raw) ----------

def get_hideout_upgrades(query, station):
    """
    Returns a list of levels with requirements:
      [ { "level": int, "requirements": [ (name, count, image), ... ] }, ... ]
    """
    data = data_store.hideout_raw or []
    station_data = next((s for s in data if s.get("name") == station), None)
    if not station_data:
        return []

    levels_out = []
    for lvl in station_data.get("levels", []):
        requirements = []
        for req in lvl.get("itemRequirements", []):
            itm = req.get("item", {})
            requirements.append((itm.get("name"), req.get("count", 0), itm.get("inspectImageLink")))
        levels_out.append({"level": lvl.get("level"), "requirements": requirements})
    return levels_out


def get_hideout_crafts(query, station):
    """
    Returns list of crafts for that station:
      [ {level, duration, requirements: [(name,count,img),...], outputs: [(name,count,img),...] }, ... ]
    """
    data = data_store.hideout_raw or []
    station_data = next((s for s in data if s.get("name") == station), None)
    if not station_data or not station_data.get("crafts"):
        return []

    crafts_out = []
    for craft in station_data.get("crafts", []):
        requirements = []
        for req in craft.get("requiredItems", []):
            it = req.get("item", {})
            requirements.append((it.get("name"), req.get("count", 0), it.get("inspectImageLink")))
        outputs = []
        for out in craft.get("rewardItems", []):
            it = out.get("item", {})
            outputs.append((it.get("name"), out.get("count", 1), it.get("inspectImageLink")))
        crafts_out.append({
            "level": craft.get("level"),
            "duration": craft.get("duration"),
            "requirements": requirements,
            "outputs": outputs
        })
    return crafts_out


# Keep CLI behaviour for local dev
if __name__ == "__main__":
    # quick local test (will be empty unless data_loader loaded)
    print("Items cached:", len(data_store.items_raw or []))
