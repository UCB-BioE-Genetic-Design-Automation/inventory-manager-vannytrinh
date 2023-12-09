from dataclasses import dataclass
from .models.concentration import Concentration
from .models.culture import Culture

@dataclass(frozen=True)
class Sample:
    label: str                  # What's written on the top of the tube
    sidelabel: str              # What's written on the side of the tube
    concentration: Concentration  # The amount or type of DNA present
    construct: str              # The name of the DNA matching the construction file
    culture: Culture = None     # For minipreps only, how many rounds of isolation
    clone: str = '0'             # Which isolate of several of the same construct