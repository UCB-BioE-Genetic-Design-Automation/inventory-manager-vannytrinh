from enum import Enum

class Concentration(Enum):
    miniprep = "miniprep"   # A plasmid miniprep
    zymo = "zymo"           # A purified DNA product
    uM100 = "uM100"         # Oligo concentration for stocks
    uM10 = "uM10"           # Oligo concentration for PCR
    uM266 = "uM266"         # Oligo concentration for sequencing
    dil20x = "dil20x"       # A diluted plasmid or other DNA
    gene = "gene"           # A gene synthesis order

    def __str__(self):
        return str(self.value)