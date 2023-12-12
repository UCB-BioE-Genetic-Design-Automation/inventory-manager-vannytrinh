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
        self.assertEqual(len(new_inventory.boxes), 1)

        # try adding a box with the same name 
        box2 = im.make_empty_box('primers1', 'another box for primers', 'minus20', (8,8))
        # should error 
        with self.assertRaises(ValueError):
            im.add_box(box2, new_inventory)

        # try adding a non-box instance
        with self.assertRaises(ValueError):
            im.add_box('fake box', new_inventory)

        # add multiple boxes
        box3 = im.make_empty_box('primers2', 'primer box', 'minus20', (8,8))
        box4 = im.make_empty_box('primers3', 'another box for primers', 'minus20', (8,8))
        new_inventory = im.add_box(box3, new_inventory)
        new_inventory = im.add_box(box4, new_inventory)
        # check number of boxes in inventory
        self.assertEqual(len(new_inventory.boxes), 3)
        self.assertIn(box3, new_inventory.boxes)
        self.assertIn(box4, new_inventory.boxes)

    def test_add_sample(self):
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

        # expected location 
        loc = Location('primers1', 0, 0, 'primer1', 'pcr primer1')

        # find location of sample
        construct_loc = inventory.construct_to_locations['p1']
        self.assertEqual(len(construct_loc), 1)
        self.assertIn(loc, construct_loc)

        # check conc, clone, culture of sample 
        conc = inventory.loc_to_conc[loc]
        self.assertEqual(conc, Concentration.uM10)

        clone = inventory.loc_to_clone[loc]
        self.assertEqual(clone, '1')

        culture = inventory.loc_to_culture[loc]
        self.assertEqual(culture, None)

        # try adding sample to same location
        with self.assertRaises(ValueError):
            im.add_sample(sample, (0, 0), 'primers1', inventory)

        # add multiple samples 
        sample2 = Sample('primer2', 'pcr primer2', Concentration.uM10, 'p2', None, '1')
        sample3 = Sample('primer3', 'pcr primer3', Concentration.uM10, 'p3', None, '1')
        inventory = im.add_sample(sample2, (0, 2), 'primers1', inventory)
        inventory = im.add_sample(sample3, (0, 3), 'primers1', inventory)

        # check inventory correctly updated 
        self.assertEqual(len(inventory.construct_to_locations), 3)
        self.assertEqual(len(inventory.loc_to_conc), 3)
        self.assertEqual(len(inventory.loc_to_clone), 3)
        self.assertEqual(len(inventory.loc_to_culture), 3)

        # add sample with existing construct
        sample4 = Sample('primer4', 'same construct as primer1', Concentration.uM10, 'p1', None, '1')
        inventory = im.add_sample(sample4, (0, 4), 'primers1', inventory)

        # check that inventory data was updated properly
        self.assertEqual(len(inventory.construct_to_locations), 3)
        self.assertEqual(len(inventory.construct_to_locations['p1']), 2)

        self.assertEqual(len(inventory.loc_to_conc), 4)
        self.assertEqual(len(inventory.loc_to_clone), 4)
        self.assertEqual(len(inventory.loc_to_culture), 4)








    # def test_add_sample(self):

    # def test_remove_box(self):
    #     im = InventoryManager()
    #     inventory = Inventory([], {}, {}, {}, {})
    #     box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
    #     inventory = im.add_box(box, inventory)
    #     inventory = im.remove_box(box, inventory)


        










        


if __name__ == '__main__':
    unittest.main()