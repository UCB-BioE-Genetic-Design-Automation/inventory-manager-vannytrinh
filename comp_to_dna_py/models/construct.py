from dataclasses import dataclass
from typing import List
from .transcript import Transcript


@dataclass(frozen=True)
class Construct:
    mRNAs: List[Transcript]
    promoter: str
    terminator: str
