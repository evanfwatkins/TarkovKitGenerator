import json
import logging
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests

from data_store import data_store

API_URL = "https://json.tarkov.dev/pve/items"
CACHE_PATH = Path.home() / ".cache" / "tarkov-kit-generator" / "pve-items-v1.json"
PROJECT_DATA_PATH = Path(__file__).resolve().parent / "data" / "pve-items.json"
CACHE_MAX_AGE = timedelta(hours=24)
HEADERS = {"Accept": "application/json"}
logger = logging.getLogger(__name__)


def _display_name(item):
    name = item.get("name")
    item_id = item.get("id")
    if isinstance(name, str) and name.strip() and name != f"{item_id} Name":
        return name

    wiki_link = item.get("wikiLink")
    if isinstance(wiki_link, str):
        wiki_name = unquote(urlsplit(wiki_link).path.rsplit("/", 1)[-1]).replace("_", " ")
        if wiki_name:
            return wiki_name

    normalized_name = item.get("normalizedName")
    if isinstance(normalized_name, str) and normalized_name:
        return re.sub(r"[-_]+", " ", normalized_name).strip().title()
    return str(item_id or "Unknown item")


def _normalize_items(items):
    if isinstance(items, dict):
        items = items.values()
    elif not isinstance(items, list):
        raise ValueError("Tarkov JSON response did not contain an item collection")

    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        item_types = item.get("types")
        if not isinstance(item_types, list):
            continue
        item_types = [item_type for item_type in item_types if isinstance(item_type, str)]
        normalized_name = item.get("normalizedName")
        if not isinstance(normalized_name, str):
            normalized_name = ""

        if not (
            {"helmet", "headphones", "rig", "armor", "backpack", "grenade", "gun"}.intersection(item_types)
            or ("mask" in normalized_name.lower() and "wearable" in item_types)
        ):
            continue

        image = item.get("inspectImageLink") or item.get("iconLink")
        normalized.append(
            {
                "id": item.get("id"),
                "name": _display_name(item),
                "normalizedName": normalized_name,
                "types": item_types,
                "inspectImageLink": image if isinstance(image, str) else None,
                "blocksHeadphones": bool(item.get("blocksHeadphones", False)),
            }
        )
    return normalized


def _read_cache():
    try:
        cached = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, None
    except (OSError, json.JSONDecodeError) as error:
        logger.warning("Unable to read Tarkov item cache: %s", error)
        return None, None

    if not isinstance(cached, dict) or not isinstance(cached.get("items"), list):
        logger.warning("Tarkov item cache has an invalid format")
        return None, None

    cached_items = [item for item in cached["items"] if isinstance(item, dict)]
    try:
        fetched_at = datetime.fromisoformat(cached["fetchedAt"])
    except (KeyError, TypeError, ValueError) as error:
        logger.warning("Tarkov item cache has an invalid timestamp: %s", error)
        return cached_items, None
    if fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=timezone.utc)
    return cached_items, fetched_at


def _write_cache(items, fetched_at):
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = CACHE_PATH.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps({"fetchedAt": fetched_at.isoformat(), "items": items}, separators=(",", ":")),
            encoding="utf-8",
        )
        temporary_path.replace(CACHE_PATH)
    except OSError as error:
        logger.warning("Unable to save Tarkov item cache: %s", error)


def _write_project_data(items, fetched_at):
    try:
        PROJECT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = PROJECT_DATA_PATH.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(
                {"fetchedAt": fetched_at.isoformat(), "source": API_URL, "items": items},
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
        temporary_path.replace(PROJECT_DATA_PATH)
    except OSError as error:
        logger.warning("Unable to update the project Tarkov data snapshot: %s", error)


def _read_project_snapshot():
    payload = json.loads(PROJECT_DATA_PATH.read_text(encoding="utf-8"))
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError(f"Invalid Tarkov data snapshot: {PROJECT_DATA_PATH}")
    try:
        fetched_at = datetime.fromisoformat(payload["fetchedAt"])
    except (KeyError, TypeError, ValueError):
        fetched_at = None
    if fetched_at is not None and fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=timezone.utc)
    return items, fetched_at


def _read_project_data():
    items, _ = _read_project_snapshot()
    return items


def _load_items():
    data_source = os.environ.get("TARKOV_DATA_SOURCE", "api").strip().lower()
    if data_source == "bundled":
        items = _read_project_data()
        logger.info("Loaded %s Tarkov items from the project snapshot", len(items))
        return items
    if data_source != "api":
        raise ValueError("TARKOV_DATA_SOURCE must be either 'api' or 'bundled'")

    cached_items, cached_at = _read_cache()
    try:
        project_items, project_at = _read_project_snapshot()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        logger.warning("Unable to read project Tarkov data snapshot: %s", error)
        project_items, project_at = None, None

    if (
        project_items is not None
        and project_at is not None
        and (cached_at is None or project_at > cached_at)
    ):
        cached_items, cached_at = project_items, project_at

    now = datetime.now(timezone.utc)
    if cached_items is not None and cached_at is not None and now - cached_at < CACHE_MAX_AGE:
        logger.info("Loaded Tarkov items from local cache")
        return cached_items

    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=60)
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            raise ValueError("Tarkov JSON response did not contain a data object")
        items = _normalize_items(data.get("items"))
    except (requests.RequestException, ValueError) as error:
        if cached_items is not None:
            logger.warning("Tarkov JSON API request failed; using cached items: %s", error)
            return cached_items
        logger.warning("Unable to load Tarkov items from JSON API: %s", error)
        return []

    _write_cache(items, now)
    _write_project_data(items, now)
    logger.info("Loaded %s Tarkov items from JSON API", len(items))
    return items


def preload_kit_data():
    items = _load_items()
    data_store.helmets = [item for item in items if "helmet" in item["types"]]
    data_store.headsets = [item for item in items if "headphones" in item["types"]]
    data_store.masks = [
        item for item in items
        if "mask" in item["normalizedName"].lower()
        and "wearable" in item["types"]
        and "helmet" not in item["types"]
    ]
    data_store.chest_rigs = [item for item in items if "rig" in item["types"]]
    data_store.armors = [
        item for item in items
        if "armor" in item["types"] and "rig" not in item["types"]
    ]
    data_store.backpacks = [item for item in items if "backpack" in item["types"]]
    data_store.grenades = [item for item in items if "grenade" in item["types"]]
    data_store.guns = [item for item in items if "gun" in item["types"]]
