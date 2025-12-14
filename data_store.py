from dataclasses import dataclass, field

"""
In-memory data store for Tarkov data loaded during app startup
"""

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