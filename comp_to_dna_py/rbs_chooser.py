from typing import List, Set
from .models.rbs_option import RBSOption


class RBSChooser:
    def __init__(self):
        self.rbs_options = [
            RBSOption(
                name="BBa_b0034",
                description="RBS based on Elowitz repressilator",
                sequence="aaagaggagaaatactag",
                protein="MASSED",
                strength=0.5
            ),
            RBSOption(
                name="BBa_b0032",
                description="RBS.3 (medium) -- derivative of BBa_0030",
                sequence="tcacacaggaaagtactag",
                protein="MTQRIA",
                strength=0.7
            ),
            RBSOption(
                name="Pbad_rbs",
                description="RBS from pBADmychisA with T7RNAP inserted",
                sequence="CCATACCCGTTTTTTTGGGCTAACAGGAGGAATTAAcc",
                protein="MDYKDDDDK",
                strength=0.9
            )
        ]

    def run(self, protein_sequence: str, ignored_options: Set[RBSOption]) -> RBSOption:
        for option in self.rbs_options:
            if option not in ignored_options:
                return option
        return None
