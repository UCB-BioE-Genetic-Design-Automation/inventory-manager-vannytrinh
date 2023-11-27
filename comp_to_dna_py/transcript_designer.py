from comp_to_dna_py import RBSChooser, RBSOption, Transcript
from typing import Set


class TranscriptDesigner:
    def __init__(self):
        self.amino_acid_to_codon = {
            'A': 'GCG', 'C': 'TGC', 'D': 'GAT', 'E': 'GAA', 'F': 'TTC',
            'G': 'GGT', 'H': 'CAC', 'I': 'ATC', 'K': 'AAA', 'L': 'CTG',
            'M': 'ATG', 'N': 'AAC', 'P': 'CCG', 'Q': 'CAG', 'R': 'CGT',
            'S': 'TCT', 'T': 'ACC', 'V': 'GTT', 'W': 'TGG', 'Y': 'TAC'
        }
        self.rbs_chooser = RBSChooser()

    def run(self, peptide: str, ignores: Set[RBSOption]) -> Transcript:
        selected_rbs = self.rbs_chooser.run(peptide, ignores)
        codons = [self.amino_acid_to_codon[aa] for aa in peptide]
        return Transcript(selected_rbs, peptide, codons)