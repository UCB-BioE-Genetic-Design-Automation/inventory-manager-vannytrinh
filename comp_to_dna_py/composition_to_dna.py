from .transcript_designer import TranscriptDesigner
from .models.composition import Composition
from .models.construct import Construct
from .models.transcript import Transcript
from .models.rbs_option import RBSOption
from typing import List, Set


class CompositionToDNA:
    def __init__(self):
        self.swo = TranscriptDesigner()

    def run(self, comp: Composition) -> Construct:
        proteins = comp.proteins
        organism = comp.host

        # Construct an mRNA for each peptide
        mRNAs = []
        ignores = set()  # type: Set[RBSOption]
        for peptide in proteins:
            mrna = self.swo.run(peptide, ignores)
            ignores.add(mrna.rbs)  # Add this rbs to excludes so it is not repeated
            mRNAs.append(mrna)

        # Construct the output dna
        out = Construct(mRNAs=mRNAs, promoter=comp.promoter, terminator=comp.terminator)
        return out
