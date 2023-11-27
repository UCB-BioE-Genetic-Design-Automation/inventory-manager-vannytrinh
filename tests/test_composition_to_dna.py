import unittest
from comp_to_dna_py import Composition, Construct
from comp_to_dna_py.composition_to_dna import CompositionToDNA


class TestCompositionToDNA(unittest.TestCase):
    def test_composition_to_dna(self):
        comp_to_dna = CompositionToDNA()
        composition = Composition(host="E. coli", promoter="pBAD", proteins=["MKTIILSYIFCLVFA", "MKTIILSYIFCLVFA"], terminator="rrnB")
        result = comp_to_dna.run(composition)
        self.assertIsInstance(result, Construct)


if __name__ == '__main__':
    unittest.main()