# data_loader.py
"""
Load the needed Tarkov API GraphQL queries once at startup.
Stores results into data_store and runs build_derived().
"""

import time
import requests
from typing import Dict, Any
from data_store import data_store

BASE_URL = "https://api.tarkov.dev/graphql"
REQUEST_TIMEOUT = 30


def post_graphql(query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
    resp = requests.post(BASE_URL, json={"query": query, "variables": variables or {}}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json().get("data", {})


def load_items():
    # Grab the fields you need. Expand here if you want more fields later.
    q = """
    {
      items {
        id
        name
        normalizedName
        shortName
        types
        inspectImageLink
        blocksHeadphones
      }
    }
    """
    data = post_graphql(q)
    return data.get("items", [])


def load_hideout():
    q = """
    {
      hideoutStations(gameMode: pve) {
        id
        name
        imageLink
        crafts {
          level
          duration
          requiredItems {
            item { id name inspectImageLink }
            count
          }
          rewardItems {
            item { id name inspectImageLink }
            count
          }
        }
        levels {
          level
          itemRequirements {
            item { id name inspectImageLink }
            count
          }
          skillRequirements { name level }
        }
      }
    }
    """
    data = post_graphql(q)
    return data.get("hideoutStations", [])


def load_maps():
    q = """
    {
      maps {
        id
        name
        normalizedName
      }
    }
    """
    data = post_graphql(q)
    return data.get("maps", [])


def load_all_data():
    start = time.time()
    print("[data_loader] Loading Tarkov data...")
    try:
        data_store.items_raw = load_items()
        data_store.hideout_raw = load_hideout()
        data_store.maps_raw = load_maps()
        data_store.build_derived()
        elapsed = time.time() - start
        print(f"[data_loader] Loaded data in {elapsed:.2f}s. Items: {len(data_store.items_raw) if data_store.items_raw else 0}")
        return True
    except Exception as e:
        print(f"[data_loader] Failed loading data: {e}", exc_info=True)
        return False
