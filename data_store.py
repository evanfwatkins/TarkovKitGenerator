# data_store.py
"""
In-memory cache for Tarkov data loaded at app startup.
Expose both pandas DataFrames for tabular ops and raw lists/dicts
for nested hideout data (crafts/upgrades).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import pandas as pd


@dataclass
class DataStore:
    items_raw: Optional[List[Dict[str, Any]]] = None
    hideout_raw: Optional[List[Dict[str, Any]]] = None
    maps_raw: Optional[List[Dict[str, Any]]] = None

    items_df: Optional[pd.DataFrame] = None
    items_by_name: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    items_by_id: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def build_derived(self):
        """Build DataFrame/lookups from the raw items list."""
        if not self.items_raw:
            self.items_df = pd.DataFrame()
            self.items_by_name = {}
            self.items_by_id = {}
            return

        self.items_df = pd.json_normalize(self.items_raw)
        if "name" in self.items_df.columns:
            self.items_df["name_lc"] = self.items_df["name"].str.lower()

        self.items_by_name = {i["name"].lower(): i for i in self.items_raw if "name" in i}
        self.items_by_id = {i["id"]: i for i in self.items_raw if "id" in i}

data_store = DataStore()