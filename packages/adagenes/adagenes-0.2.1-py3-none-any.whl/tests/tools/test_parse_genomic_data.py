import unittest
import adagenes as ag


class ParseGenomicDataTestCase(unittest.TestCase):

    def test_parse_aa_exchange(self):
        ref, pos, alt = ag.parse_variant_exchange("V600E")

        self.assertEqual(ref, "V","")
        self.assertEqual(pos, "600", "")
        self.assertEqual(alt, "E", "")

