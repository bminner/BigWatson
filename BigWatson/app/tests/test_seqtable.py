from ..NLU.seqtable import SeqTable
from django.test import TestCase

class SeqTableTest(TestCase):

    def test_seqtable_lookup_single_item(self):
        table = SeqTable(["Hello"])
        s, s_ind, r_ind = table.lookup(2)
        self.assertEqual(s, "Hello")
        self.assertEqual(s_ind, 0)
        self.assertEqual(r_ind, 2)

    def test_seqtable_lookup_multi_item_1(self):
        table = SeqTable(["Hello", "World", "I", "Am", "SeqTable"])
        s, s_ind, r_ind = table.lookup(5)
        self.assertEqual(s, "World")
        self.assertEqual(s_ind, 1)
        self.assertEqual(r_ind, 0)

    def test_seqtable_lookup_multi_item_2(self):
        table = SeqTable(["Hello", "World", "I", "Am", "SeqTable"])
        s, s_ind, r_ind = table.lookup(15)
        self.assertEqual(s, "SeqTable")
        self.assertEqual(s_ind, 4)
        self.assertEqual(r_ind, 2)
