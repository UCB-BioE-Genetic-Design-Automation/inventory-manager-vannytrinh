import unittest
from comp_to_dna_py import Transcript
from comp_to_dna_py.transcript_designer import TranscriptDesigner


class TestTranscriptDesigner(unittest.TestCase):
    def test_transcript_designer(self):
        designer = TranscriptDesigner()
        peptide = "MKTIIALSYIFCLVFA"
        result = designer.run(peptide, set())
        self.assertIsInstance(result, Transcript)
        self.assertEqual(result.peptide, peptide)
        self.assertIsInstance(result.codons, list)


if __name__ == '__main__':
    unittest.main()