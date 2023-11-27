from dataclasses import dataclass
from typing import List
from .host import Host


@dataclass(frozen=True)
class Composition:
    host: Host
    promoter: str
    proteins: List[str]
    terminator: str
