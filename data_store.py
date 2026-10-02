from dataclasses import dataclass, field
from typing import Any

"""
In-memory data store for Tarkov data loaded during app startup
"""

@dataclass
class DataStore:
    helmets: list[dict[str, Any]] = field(default_factory=list)
    headsets: list[dict[str, Any]] = field(default_factory=list)
    masks: list[dict[str, Any]] = field(default_factory=list)
    chest_rigs: list[dict[str, Any]] = field(default_factory=list)
    armors: list[dict[str, Any]] = field(default_factory=list)
    backpacks: list[dict[str, Any]] = field(default_factory=list)
    grenades: list[dict[str, Any]] = field(default_factory=list)
    guns: list[dict[str, Any]] = field(default_factory=list)

data_store = DataStore()