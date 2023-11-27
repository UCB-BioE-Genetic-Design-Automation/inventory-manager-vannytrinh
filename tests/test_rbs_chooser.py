import unittest
from comp_to_dna_py import RBSOption
from comp_to_dna_py.rbs_chooser import RBSChooser


class TestRBSChooser(unittest.TestCase):
    def test_rbs_chooser(self):
        chooser = RBSChooser()
        protein_sequence = "MKTIIALSYIFCLVFA"
        result = chooser.run(protein_sequence, set())
        self.assertIsInstance(result, RBSOption)


if __name__ == '__main__':
    unittest.main()