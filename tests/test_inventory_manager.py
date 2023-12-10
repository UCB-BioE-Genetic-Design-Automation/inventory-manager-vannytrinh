import unittest
from inventory_manager_py import Inventory, Box, Sample, Location, Culture, Concentration
from inventory_manager_py.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def test_make_box(self):
        im = InventoryManager()
        new_box = im.make_empty_box('Box0', 'box for primers', 'minus20', (3,4))
        self.assertIsInstance(new_box, Box)
        self.assertEqual(new_box.name, 'Box0')
        self.assertEqual(new_box.description, 'box for primers')
        self.assertEqual(new_box.location, 'minus20')
        self.assertEqual(len(new_box.samples), 3)
        self.assertEqual(len(new_box.samples[0]), 4)

    def test_add_box(self):
        im = InventoryManager()
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))

        new_inventory = im.add_box(box, inventory)

        # Check that old inventory isn't changed 
        # note: is this necessary 
        self.assertEqual(len(inventory.boxes), 0)

        # Check new inventory is an Inventory 
        self.assertIsInstance(new_inventory, Inventory)
        # Check that box was added 
        self.assertEqual(new_inventory.boxes[0], box)
    
    def test(self):
        im = InventoryManager()
        # make inventory, box, sample
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
        sample = Sample('primer1', 'pcr primer1', Concentration.uM10, 'p1', None, '1')

        # add box to inventory 
        inventory = im.add_box(box, inventory)
        # add sample to inventory
        inventory = im.add_sample(sample, (0, 0), 'primers1', inventory)
        # check box has a sample at (0,0)
        check_sample = box.samples[0][0]
        self.assertEqual(check_sample, sample)

        # try adding sample to same location
        with self.assertRaises(ValueError):
             im.add_sample(sample, (0, 0), 'primers1', inventory)

        # remove sample
        im.remove_sample((0, 0), 'primers1', inventory)
        check_sample = box.samples[0][0]
        self.assertIsNone(check_sample)








    # def test_add_sample(self):

    # def test_remove_box(self):
    #     im = InventoryManager()
    #     inventory = Inventory([], {}, {}, {}, {})
    #     box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
    #     inventory = im.add_box(box, inventory)
    #     inventory = im.remove_box(box, inventory)


        










        


if __name__ == '__main__':
    unittest.main()