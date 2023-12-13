from .models.box import Box
from .models.concentration import Concentration
from .models.culture import Culture
from .models.inventory import Inventory
from .models.location import Location
from .models.sample import Sample
from typing import List, Dict, Set, Tuple
import csv
import re 

class InventoryManager: 

    # HELPER FUNC
    def _find_box(self, boxname: str, inventory: Inventory) -> Box: 
        '''
        Finds box in inventory with given name

        Args: 
        boxname (str): name of box to search for 
        inventory (Inventory): inventory to seach for box for

        Returns: 
        Box: box with boxname or None if no box found
        '''
        # iter through boxes in inventory
        for box in inventory.boxes: 
            # check box name
            if box.name == boxname: 
                return box   
        return None

    # HELPER FUNC
    def _check_valid_location(self, box: Box, position: tuple[int, int]): 
        '''
        Check to make sure Box has given position
        '''
        # make sure location is a positive number
        row, col = position
        if row < 0 or col < 0:
            raise ValueError('Location must be positive')
        
        # get dimensions of box 
        num_row, num_col = box.get_size()
        # make sure location within range of box 
        if row >= num_row or col >= num_col:
            raise ValueError('Location does not exist in box')    

    def add_sample(self, sample: Sample, position: tuple[int, int], boxname: str, inventory: Inventory) -> Inventory: 
        '''
        Add new sample to specified location of box and updates inventory
        
        Args: 
        sample (Sample): Sample to add
        position (tuple[int, int]): Row and column position of box to add sample to 
        boxname (str): Name of box to add sample to 
        inventory (Inventory): Current inventory 
        
        Return: 
        Inventory: Updated inventory with sample added 
        '''
        # values for updated inventory
        boxes = inventory.boxes.copy()
        construct_to_locs = inventory.construct_to_locations.copy()
        loc_to_conc = inventory.loc_to_conc.copy()
        loc_to_clone = inventory.loc_to_clone.copy()
        loc_to_culture = inventory.loc_to_culture.copy()
        
        # find box 
        box = self._find_box(boxname, inventory)
        # error if box not found
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')

        # check if location is valid 
        self._check_valid_location(box, position)
        # check if location is available for sample
        if box.samples[position[0]][position[1]]: 
            raise ValueError('Location not empty')
        
        # add sample to box's samples
        updated_samples = box.samples
        updated_samples[position[0]][position[1]] = sample
        # create updated box 
        updated_box = Box(box.name, box.description, box.location, updated_samples)
        
        # remove old box from list of boxes (do not remove samples)
        boxes.remove(box)
        # switch out old box for new box 
        boxes.append(updated_box)

        # create new Location for sample  
        loc = Location(boxname, position[0], position[1], sample.label, sample.sidelabel)
        
        # update info for inventory 
        # make new set if doens't exist 
        if sample.construct not in construct_to_locs: 
            construct_to_locs[sample.construct] = set()
        construct_to_locs[sample.construct].add(loc)
        loc_to_conc[loc] = sample.concentration
        loc_to_clone[loc] = sample.clone
        loc_to_culture[loc] = sample.culture
        
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)

    def remove_sample(self, position: tuple[int, int], boxname: str, inventory: Inventory):
        '''
        Remove sample from specified location of box and updates inventory
        
        Args: 
        position (tuple[int, int]): Row and column position of box where sample is to be removed
        boxname (str): Name of box to remove sample from 
        inventory (Inventory): Current inventory 
        
        Return: 
        Inventory: Updated inventory with sample removed 
        '''
        # values of new inventory
        boxes = inventory.boxes
        construct_to_locs = inventory.construct_to_locations
        loc_to_conc = inventory.loc_to_conc
        loc_to_clone = inventory.loc_to_clone
        loc_to_culture = inventory.loc_to_culture
        
        # find box, will error if box not found
        box = self._find_box(boxname, inventory)
        # error if box not found
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')
        
        # check if location is valid 
        self._check_valid_location(box, position)
        # check if location contains a sample
        if box.samples[position[0]][position[1]] == None: 
            raise ValueError('Location is empty')
            
        # find sample 
        sample = box.samples[position[0]][position[1]]

        # remove sample from box's samples
        updated_samples = box.samples
        updated_samples[position[0]][position[1]] = None
        # create updated box 
        updated_box = Box(box.name, box.description, box.location, updated_samples)
        
        # remove old box from list of boxes (do not remove samples)
        boxes.remove(box)
        # update box
        boxes.append(updated_box)
        
        # define sample location 
        loc = Location(box.name, position[0], position[1], sample.label, sample.sidelabel)
        # remove sample info from inventory
        construct_to_locs[sample.construct].remove(loc)
        # delete entry if now empty set 
        if len(construct_to_locs[sample.construct]) == 0:
            del construct_to_locs[sample.construct]
        del loc_to_conc[loc] 
        del loc_to_clone[loc] 
        del loc_to_culture[loc]
        
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)  
    
    def find_sample(self, query: dict, inventory: Inventory) -> List[Location]: 
        '''
        Finds the locations of samples matching the given criteria within the inventory
        
        Args: 
        query (dict): Dictionary of keys corresponding to fields of a Sample 
        ('label', 'sidelabel', 'concentration', 'culture', 'clone')
        inventpry (Inventory): Current inventory
        
        Return: 
        List[Location]: List of location objects for found samples
        '''
        matches = set()

        # make sure al keys in query are sample attributes 
        valid_keys = {'label', 'sidelabel', 'concentration', 'construct', 'culture', 'clone'}
        # check if query has invalid keys
        if set(query.keys()) - valid_keys:
            raise ValueError('Can only search for sample attributes')

        # iter through all boxes in inventory
        for box in inventory.boxes:
            # iter through rows of box
            for row_idx, row in enumerate(box.samples):
                # iter through samples in row
                for col_idx, sample in enumerate(row):
                    # if None
                    if not sample:
                        continue

                    # check if sample matches query 
                    if all(getattr(sample, key, None) == value for key, value in query.items()):
                        # get location of sample
                        location = Location(
                            boxname=box.name,
                            row=row_idx,
                            col=col_idx,
                            label=sample.label,
                            sidelabel=sample.sidelabel
                        )
                        # append to result
                        matches.add(location)

        return list(matches) 

    def add_box(self, box: Box, inventory: Inventory) -> Inventory:
        '''
        Add box to inventory
        
        Args: 
        box (Box): Box instance to add to inventory 
        inventory (Inventory): Inventory instance to add box to 
        
        Returns: 
        Inventory: Updated Inventory instance with box added 
        
        '''
        # values of new inventory
        boxes = inventory.boxes.copy()
        construct_to_locs = inventory.construct_to_locations.copy()
        loc_to_conc = inventory.loc_to_conc.copy()
        loc_to_clone = inventory.loc_to_clone.copy()
        loc_to_culture = inventory.loc_to_culture.copy()

        # check inputs
        if not isinstance(box, Box): 
            raise ValueError('Invalid box')
        if not isinstance(inventory, Inventory):
            raise ValueError('Invalid inventory')

        # check that box with same name does not already exist 
        if self._find_box(box.name, inventory):
            raise ValueError(f'Box with name {box.name} already exist in inventory')

        # add box
        boxes.append(box)
        
        # iter through each sample in box 
        # add sample to inventory 
        samples = box.samples
        # iter through rows
        for i in range(len(samples)): 
            # iter through item in row 
            for j in range(len(samples[i])): 
                if samples[i][j]:
                    sample = samples[i][j]
                    # define sample location 
                    loc = Location(boxname=box.name, row=i, col=j, 
                                label=sample.label, sidelabel=sample.sidelabel) 
                    # make new set if doens't exist 
                    if sample.construct not in construct_to_locs: 
                        construct_to_locs[sample.construct] = set()
                    construct_to_locs[sample.construct].add(loc)
                    loc_to_conc[loc] = sample.concentration
                    loc_to_clone[loc] = sample.clone
                    loc_to_culture[loc] = sample.culture
                        
        # return new inventory with updated info 
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)
    
    def remove_box(self, boxname: str, inventory: Inventory) -> Inventory:
        '''
        Remove box with given name from inventory
        
        Args: 
        boxname (str): name of box to remove from inventory 
        inventory (Inventory): Inventory instance to remove box from 
        
        Returns: 
        Inventory: Updated Inventory instance with box removed  
        
        '''
        # new attributes of inventory
        boxes = inventory.boxes
        construct_to_locs = inventory.construct_to_locations
        loc_to_conc = inventory.loc_to_conc
        loc_to_clone = inventory.loc_to_clone
        loc_to_culture = inventory.loc_to_culture
        
        # find box
        box = self._find_box(boxname, inventory)
        # error if box not found
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')
        
        samples = box.samples
        # for each sample in box
        # remove sample from iventory 
        # iter through rows
        for i in range(len(samples)): 
            # iter through item in row 
            for j in range(len(samples[i])): 
                if samples[i][j]:
                    sample = samples[i][j]
                    # define sample location 
                    loc = Location(boxname=box.name, row=i, col=j, 
                                label=sample.label, sidelabel=sample.sidelabel)
                    
                    construct_to_locs[sample.construct].remove(loc)
                    # delete entry if now empty set 
                    if len(construct_to_locs[sample.construct]) == 0:
                        del construct_to_locs[sample.construct]
                    del loc_to_conc[loc] 
                    del loc_to_clone[loc] 
                    del loc_to_culture[loc]
                    
        # remove box 
        boxes.remove(box)
        
        # return new inventory with updated info 
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)

    def update_box(self, boxname, updates, inventory) -> Inventory: 
        '''
        Updates specified metadata fields of box and updates inventory 
        
        Args: 
        boxnam (str): Name of box to be updated 
        updates (dict): Dictionary of keys corresponding to box fields to be updated 
        with new values ('name', 'description', 'location')
        inventpry (Inventory): Current inventory 
        
        Return:
        Inventory: Updated inventory 
        '''
        # Find the box to be updated
        box = self._find_box(boxname, inventory)
        # Check that box exists
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')
        
        # Update fields with new values or keep existing values
        name = updates.get('name', box.name)
        description = updates.get('description', box.description)
        location = updates.get('location', box.location)
        
        # Create the updated box
        updated_box = Box(name, description, location, box.samples)

        # If the name was changed, update sample locations
        if name != box.name:
            # Remove the old box
            inventory = self.remove_box(box.name, inventory)
            # Add the updated box to the inventory
            return self.add_box(updated_box, inventory)
        else:
            # If the name hasn't changed, update the box in place
            boxes = inventory.boxes.copy()
            boxes.remove(box)
            boxes.append(updated_box)
            return Inventory(
                boxes,
                inventory.construct_to_locations,
                inventory.loc_to_conc,
                inventory.loc_to_clone,
                inventory.loc_to_culture
            )

    def retrieve_box_contents(self, boxname: str, inventory: Inventory):
        '''
        Retrieves contents of specified box
        
        Args: 
        boxname (str): Name of box whose contents are to be retrieved
        inventory (Inventory): Current inventory 
        
        Return:
        List[List[Sample]]: Content of specified box structured as 
        2D array corresponding to layout of box
        '''
        box = self._find_box(boxname, inventory)
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')
        return box.samples

    # NOTE: make sure box instance is not changed after
    def box_to_tsv(self, box: Box, filepath: str) -> str: 
        '''
        Saves data of specified box to TSV format and saves it as a file
        
        Args:
        box (Box): Box whose data is to be converted
        filepath (str): Filepath wheer tsv is to be stored
        
        Return:
        str: name of filepath where tsv was saved
        '''
        # HELPER FUNCTION
        def calc_row_label(self, num_row: int) -> str:
            '''
            Calculates the letter equivalent of a row number using zero-based numbering
            (eg. 'A' for row 0)

            Arg:
            num_row (int): Row integer 

            Return:
            str: Letter equivalent of row number 
            '''
            if num_row < 0:
                raise ValueError('Row number must be non-negative')
                
            result = ""
            while num_row >= 0:
                # Convert the remainder to the corresponding letter
                char_value = num_row % 26
                result = chr(ord('A') + char_value) + result
                # Update the number for the next iteration
                num_row = num_row // 26 - 1

                if num_row < 0:
                    break
            
            return result

        # helper function to format attribute of samples for tsv 
        def format_sample_tsv(samples, attr):
            # make sure not to change Box instance
            samples_tsv = samples.copy()

            # iter through rows
            for irow, row in enumerate(samples_tsv):
                row_tsv = row.copy()
                # iter through samples
                for icol, sample in enumerate(row_tsv):
                    # if sample exists
                    if sample:
                        # get the attr 
                        sample_attr = getattr(sample, attr)
                        # check if it is not none
                        if sample_attr:
                            # get string of attr 
                            # don't want to get the string of none
                            # want the string of Enum classes 
                            sample_attr = str(sample_attr)
                        row_tsv[icol] = sample_attr
                # add row label to array 
                row_tsv.insert(0, calc_row_label(irow))
                samples_tsv[irow] = row_tsv

            # create header for array
            header = [f'>>{attr}'] + [i for i in range(1, len(samples_tsv[0]))]
            samples_tsv.insert(0, header)

            return samples_tsv
        
        # list of rows for tsv file
        tsv_info = []
        
        # append box metadata 
        tsv_info.append(['>name', box.name])
        tsv_info.append(['>description', box.description])
        tsv_info.append(['>location', box.location])
        tsv_info.append([])
        
        # attributes to include in tsv file
        attrs = ['label', 'sidelabel', 'concentration', 'construct', 'culture', 'clone']
        # append sample info
        for attr in attrs:
            tsv_info.extend(format_sample_tsv(samples, attr))
            tsv_info.append([])
        
        # write to file
        # will error if unable to access filepath
        with open(filepath, 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerows(tsv_info)
        
        return filepath

    def tsv_to_box(self, filepath):
        '''
        Converts data from TSV file into Box object 
        
        Args:
        filepath (str): filepath of TSV to be converted
        
        Return:
        Box: Box object created from TSV file
        '''
        # HELPER FUNCTION
        def calc_row_num(self, row_label: str) -> int:
            '''
            Calulate a row label into a number (eg. 'A' -> 0, 'B' -> 1, 'AA' -> 26)

            Arg:
            row_label (str): Row label made of uppercase letters

            Return:
            int: Integer equivalent of row label, using 0-based numbering

            '''
            result = 0
            for char in row_label:
                result = result * 26 + (ord(char) - ord('A') + 1)
            return result - 1  # Adjusting to 0-based index

        # read tsv file
        # will error if unable to find/open file
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')
                # Read the entire content into a list
                tsv_data = list(reader)

        # dict to describe box
        box_dict = {}
        # array (will become 2d array) to keep track of sample data
        samples = []
        # num of columns in a box 
        num_col = None
        # current attribute being parsed 
        curr_attr = None

        # parse through row in data
        for row in tsv_data:
            # skip empty rows
            if row == []:
                continue

            # look for '>' indicating box data
            if row[0][0] == '>' and row[0][1] != '>':
                # make sure there is a value for attribute
                if len(row) != 2:
                    raise ValueError('Box metadata incorrectly entered')
                # get name of attribute
                attr_name = row[0][1:]
                # get value of attribute
                attr_val = row[1]
                # add info to box dict 
                box_dict[attr_name] = attr_val

            # look for '>>' indicating 
            if row[0][0:2] == '>>':
                # if not defined yet, set the number of col in a box
                # Note: num_col includes the row label as an col 
                if num_col == None:
                    num_col = len(row)

                # check that the num of cols in row matches the num cols for box
                if  num_col != len(row):
                    raise ValueError('Number of columns do not match for all rows')

                # set the current attribute
                curr_attr = row[0][2:]

            # check if row starts with row label 
            if is_valid_row_label(row[0]):
                # check that row has the correct number of cols in it
                if num_col != len(row):
                    raise ValueError('Number of columns do not match for all rows')

                # get row number 
                irow = calc_row_num(row[0])
                # check if this row either already exists or if it is the next row 
                # if it is not the next row then data is formatted incorrectly and a row was skipped
                if irow > len(samples): 
                    raise ValueError('Row labels do not match number of rows given')

                # if row not added yet 
                if irow == len(samples):
                    # define row 
                    new_row = []
                    # add empty dictionaries for each column
                    for i in range(num_col - 1):
                        new_row.append({})
                    # add row
                    samples.append(new_row)

                # iter through samples in row 
                for icol, sample in enumerate(row[1:]):  
                    # if there is sample data
                    if sample:
                        # add it to dict 
                        sample_dict = samples[irow][icol]
                        sample_dict[curr_attr] = sample 
                        
        # to store Sample objects in 2d array
        final_samples = []  

        # iter through the rows of samples
        for irow, row in enumerate(samples):

            # add row to final array
            final_samples.append([])

            # iter through samples in row
            for sample in row:

                # if there is data in sample dict
                if len(sample) > 0:
                    # turn dict into Sample object
                    sample = Sample(**sample)
                else:
                    sample = None
                final_samples[irow].append(sample)
                
        # add final array of samples to box dict 
        box_dict['samples'] = final_samples

        # create new dict
        return Box(**box_dict)
    
    def make_empty_box(self, name: str, description: str, location: str, size: tuple[str, str]) -> Box:
        '''
        Creates box of given size
        '''
        # get size of box from input
        num_row, num_col = size
        # size must be at least 1
        if num_row < 1:
            raise ValueError('Must have at least 1 row')
        if num_col < 1:
            raise ValueError('Must have at least 1 column')
            
        def empty_samples(num_row: int, num_col: int): 
            '''
            Returns a num_row by num_col matrix of nones
            '''
            row = [None] * num_col 
            samples = [row.copy() for i in range(num_row)]
            return samples
        
        samples = empty_samples(num_row, num_col)
        
        return Box(name, description, location, samples)