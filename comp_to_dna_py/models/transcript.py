from dataclasses import dataclass
from .rbs_option import RBSOption


@dataclass(frozen=True)
class Transcript:
    rbs: RBSOption
    peptide: str
    codons: list[str]
