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
    helmets: list = field(default_factory=list)
    headsets: list = field(default_factory=list)
    masks: list = field(default_factory=list)
    chest_rigs: list = field(default_factory=list)
    armors: list = field(default_factory=list)
    backpacks: list = field(default_factory=list)
    grenades: list = field(default_factory=list)
    guns: list = field(default_factory=list)

data_store = DataStore()
