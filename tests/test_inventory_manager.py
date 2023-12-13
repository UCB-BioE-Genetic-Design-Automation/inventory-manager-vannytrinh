import unittest
from inventory_manager_py import Inventory, Box, Sample, Location, Culture, Concentration
from inventory_manager_py.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def test_make_box(self):
        im = InventoryManager()
        # create empty box
        new_box = im.make_empty_box('Box0', 'box for primers', 'minus20', (3,4))

        # check if return value is a Box instance
        self.assertIsInstance(new_box, Box)
        # check that the name, description, location of the box is correct
        self.assertEqual(new_box.name, 'Box0')
        self.assertEqual(new_box.description, 'box for primers')
        self.assertEqual(new_box.location, 'minus20')

        # check number of rows
        self.assertEqual(len(new_box.samples), 3)
        # check number of columns
        self.assertEqual(len(new_box.samples[0]), 4)

    def test_add_box(self):
        im = InventoryManager()
        # create inventory and empty box
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))

        # add empty box to inventory 
        new_inventory = im.add_box(box, inventory)

        # check that old inventory isn't changed 
        # Note: is this necessary?
        self.assertEqual(len(inventory.boxes), 0)

        # check new inventory is an Inventory instance
        self.assertIsInstance(new_inventory, Inventory)
        # check that box was added to inventory
        num_boxes = len(new_inventory.boxes)
        self.assertEqual(num_boxes, 1)
        self.assertEqual(new_inventory.boxes[0], box)

        # try adding a box with the same name 
        box2 = im.make_empty_box('primers1', 'another box for primers', 'minus20', (8,8))
        # should error 
        with self.assertRaises(ValueError):
            im.add_box(box2, new_inventory)

        # try adding a non-box instance
        # should error
        with self.assertRaises(ValueError):
            im.add_box('fake box', new_inventory)

        # add multiple boxes to inventory
        box3 = im.make_empty_box('primers2', 'primer box', 'minus20', (8,8))
        box4 = im.make_empty_box('primers3', 'another box for primers', 'minus20', (8,8))
        new_inventory = im.add_box(box3, new_inventory)
        new_inventory = im.add_box(box4, new_inventory)
        # check that new boxes are in inventory
        num_boxes = len(new_inventory.boxes)
        self.assertEqual(num_boxes, 3)
        self.assertIn(box3, new_inventory.boxes)
        self.assertIn(box4, new_inventory.boxes)

    def test_add_sample(self):
        im = InventoryManager()
        # make inventory, box, sample
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
        sample = Sample('primer1', 'pcr primer1', Concentration.uM10, 'p1', None, '1')

        # add box, sample to inventory 
        inventory = im.add_box(box, inventory)
        inventory = im.add_sample(sample, (0, 0), 'primers1', inventory)
        # check box has a sample at (0,0)
        check_sample = box.samples[0][0]
        self.assertEqual(check_sample, sample)

        # define expected location 
        loc = Location('primers1', 0, 0, 'primer1', 'pcr primer1')
        # find location of sample
        construct_loc = inventory.construct_to_locations['p1']

        # there should be one location
        self.assertEqual(len(construct_loc), 1)
        # check that it is the right location
        self.assertIn(loc, construct_loc)
        # check conc, clone, culture of sample 
        conc = inventory.loc_to_conc[loc]
        clone = inventory.loc_to_clone[loc]
        culture = inventory.loc_to_culture[loc]

        # check that the concentration, clone, culture of the sample is correct
        self.assertEqual(conc, Concentration.uM10)
        self.assertEqual(clone, '1')
        self.assertEqual(culture, None)

        # try adding a sample to occupied location
        # should error
        with self.assertRaises(ValueError):
            im.add_sample(sample, (0, 0), 'primers1', inventory)

        # try adding to a location out of bounds
        # should error
        with self.assertRaises(ValueError):
            im.add_sample(sample, (100, 100), 'primers1', inventory)

        # try adding to a box that isn't in the inventory 
        # should error
        with self.assertRaises(ValueError):
            im.add_sample(sample, (1, 1), 'primers', inventory)

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

    def test_remove_box(self):
        im = InventoryManager()
        # create inventory, box, sample
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
        sample = Sample('primer1', 'pcr primer1', Concentration.uM10, 'p1', None, '1')

        # add box, sample to inventory
        inventory = im.add_box(box, inventory)
        inventory = im.add_sample(sample, (0,0), 'primers1', inventory)
        
        # remove box
        inventory = im.remove_box('primers1', inventory)

        # check that box removed
        num_boxes = len(inventory.boxes)
        self.assertEqual(num_boxes, 0) 

        # check that sample information removed
        num_cons = len(inventory.construct_to_locations)
        self.assertEqual(num_cons, 0)
        self.assertEqual(len(inventory.loc_to_conc), 0)
        self.assertEqual(len(inventory.loc_to_clone), 0)
        self.assertEqual(len(inventory.loc_to_culture), 0)

    def test_remove_sample(self):
        im = InventoryManager()
        # create inventory, box, sample
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
        sample = Sample('primer1', 'pcr primer1', Concentration.uM10, 'p1', None, '1')

        # add box, sample
        inventory = im.add_box(box, inventory)
        inventory = im.add_sample(sample, (0, 0), 'primers1', inventory)

        # remove sample
        inventory = im.remove_sample((0,0), 'primers1', inventory)
        
        # check that location is empty 
        self.assertIsNone(box.samples[0][0])

        # check that inventory is updated 
        num_cons = len(inventory.construct_to_locations)
        self.assertEqual(num_cons, 0)
        self.assertEqual(len(inventory.loc_to_conc), 0)
        self.assertEqual(len(inventory.loc_to_clone), 0)
        self.assertEqual(len(inventory.loc_to_culture), 0)

        # try removing the sample again 
        # should error
        with self.assertRaises(ValueError):
            im.remove_sample((0,0), 'primers1', inventory)

        # try removing something out of bounds 
        # should error
        with self.assertRaises(ValueError):
            im.remove_sample((100, 100), 'primers1', inventory)

        # try removing from a box that isn't in the inventory 
        # should error
        with self.assertRaises(ValueError):
            im.remove_sample((1, 1), 'primers', inventory)
    
    def test_find_sample(self): 
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

        # find specific sample
        query0 = {'label': 'p1', 
                    'sidelabel': 'pcr primer1', 
                    'concentration': Concentration.uM10, 
                    'construct': 'o1', 
                    'culture': None, 
                    'clone': '1'}
        query0_result = im.find_sample(query0, inventory)
        # check for one location returned
        self.assertEqual(len(query0_result), 1)
        loc0 = query0_result[0]
        # check location is correct 
        self.assertEqual(loc0.boxname, 'primers1')
        self.assertEqual(loc0.row, 0)
        self.assertEqual(loc0.col, 0)
        self.assertEqual(loc0.label, 'p1')
        self.assertEqual(loc0.sidelabel, 'pcr primer1')

        # find samples w/ concentration uM10
        query1 = {'concentration' : Concentration.uM10}
        query1_result = im.find_sample(query1, inventory)
        # check for correct number of locations returned
        self.assertEqual(len(query1_result), 3)

        # find sample w/ construct 'o1'
        query2 = {'construct': 'o1'}
        query2_result = im.find_sample(query2, inventory)
        # check for correct number of locations returned
        self.assertEqual(len(query2_result), 3)

        # find sample w/ concentration uM10, construct 'o1'
        query3 = {'concentration' : Concentration.uM10,
                    'construct': 'o1'}
        query3_result = im.find_sample(query3, inventory)
        # check for correct number of locations returned
        self.assertEqual(len(query3_result), 1)

        # find sample that doesn't exist
        query4 = {'label' : 'dna sample'}
        query4_result = im.find_sample(query4, inventory)
        # check that no samples found
        self.assertEqual(len(query4_result), 0)

        # use invalid key 
        # should error
        query5 = {'boxname' : 'primers1'}
        with self.assertRaises(ValueError):
            im.find_sample(query5, inventory)

    def test_update_box(self):
        im = InventoryManager()
        # create inventory, box, sample
        inventory = Inventory([], {}, {}, {}, {})
        box = im.make_empty_box('primers1', 'box for primers', 'minus20', (8,8))
        sample = Sample('primer1', 'pcr primer1', Concentration.uM10, 'p1', None, '1')

        # add sample
        inventory = im.add_box(box, inventory)
        inventory = im.add_sample(sample, (0, 0), 'primers1', inventory)

        # define box updates
        updates = {'name': 'pcr primers', 'description': 'pcr primer box'}
        # udpate box 
        inventory = im.update_box('primers1', updates, inventory)

        # check description of box in inventory is updated
        box = inventory.boxes[0]
        self.assertEqual(box.name, 'pcr primers')
        self.assertEqual(box.description, 'pcr primer box')
        self.assertEqual(box.location, 'minus20')

        # check that sample location is updated 
        self.assertEqual(len(inventory.construct_to_locations['p1']), 1)
        loc = inventory.construct_to_locations['p1'].copy().pop()
        self.assertEqual(loc.boxname, 'pcr primers')
        # check that other dictionaries have been updated w/ new location 
        self.assertIn(loc, inventory.loc_to_conc)
        self.assertIn(loc, inventory.loc_to_clone)
        self.assertIn(loc, inventory.loc_to_culture)
        # check that dictionaries only contain new location
        self.assertEqual(len(inventory.loc_to_conc), 1)
        self.assertEqual(len(inventory.loc_to_clone), 1)
        self.assertEqual(len(inventory.loc_to_culture), 1)

    def test_retrieve_box(self):
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
    
        # check for an 8x8 2d array 
        box_samples = im.retrieve_box_contents('primers1', inventory)
        self.assertIsInstance(box_samples, list)
        self.assertEqual(len(box_samples), 8) 
        self.assertIsInstance(box_samples[0], list)
        self.assertEqual(len(box_samples[0]), 8)

        # check each sample is correct
        box_sample1 = box_samples[0][0]
        box_sample2 = box_samples[0][1]
        box_sample3 = box_samples[0][2]
        box_sample4 = box_samples[0][3]
        box_sample5 = box_samples[0][4]
        box_sample6 = box_samples[0][5]

        self.assertEqual(box_sample1, sample1)
        self.assertEqual(box_sample2, sample2)
        self.assertEqual(box_sample3, sample3)
        self.assertEqual(box_sample4, sample4)
        self.assertEqual(box_sample5, sample5)
        self.assertEqual(box_sample6, sample6)

if __name__ == '__main__':
    unittest.main()