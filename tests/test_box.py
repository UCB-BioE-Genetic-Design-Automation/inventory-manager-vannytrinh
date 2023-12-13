import unittest
from inventory_manager_py import Inventory, Box, Sample, Location, Culture, Concentration
from inventory_manager_py.inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):
    def test_get_size(self):
        im = InventoryManager()
        # create empty box
        box = im.make_empty_box('Box0', 'box for primers', 'minus20', (3,4))

        # get size of box
        num_row, num_col = box.get_size()

        # check sizes 
        self.assertEqual(num_row, 3)
        self.assertEqual(num_col, 4)

    def test_get_num_samples(self):
        im = InventoryManager()
        # create inventory, box, samples
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))

        sample1 = Sample('p1', 'pcr primer1', Concentration.uM10, 'o1', None, '1')
        sample2 = Sample('p2', 'pcr primer2', Concentration.uM10, 'o2', None, '1')
        sample3 = Sample('p3', 'pcr primer3', Concentration.uM10, 'o3', None, '1')
        sample4 = Sample('st1', 'stock primer1', Concentration.uM100, 'o1', None, '1')
        sample5 = Sample('st2', 'stock primer2', Concentration.uM100, 'o2', None, '1')
        sample6 = Sample('seq1', 'seq primer1', Concentration.uM266, 'o1', None, '1')
        samples = [sample1, sample2, sample3, sample4, sample5, sample6]

        # add samples
        inventory = im.add_box(box, inventory)
        for i, sample in enumerate(samples):
            inventory = im.add_sample(sample, (0, i), 'primers1', inventory) 
        
        # get updated box from inventory
        box = inventory.boxes[0]
        num_samples = box.get_num_samples()

        # check result
        self.assertEqual(num_samples, 6)