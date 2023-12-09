from dataclasses import dataclass
from typing import List, Dict, Set
from .box import Box
from .location import Location
from .concentration import Concentration
from .culture import Culture

@dataclass(frozen=True)
class Inventory:
    boxes: List[Box]                                   # all the boxes in the inventory
    construct_to_locations: Dict[str, Set[Location]]   # Quick lookup of samples by construct name
    loc_to_conc: Dict[Location, Concentration]         # Quick lookup by Concentration
    loc_to_clone: Dict[Location, str]                  # Quick lookup by Clone
    loc_to_culture: Dict[Location, Culture]            # Quick lookup by Culture