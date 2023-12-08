from .models.box import Box
from .models.concentration import Concentration
from .models.culture import Culture
from .models.inventory import Inventory
from .models.location import Location
from .models.sample import Sample
from typing import List, Dict, Set, Tuple

class InventoryManager: 

    def add_sample(sample: Sample, position: tuple[int, int], boxname: str, inventory: Inventory) -> Inventory: 
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
        boxes = inventory.boxes
        construct_to_locs = inventory.construct_to_locations
        loc_to_conc = inventory.loc_to_conc
        loc_to_clone = inventory.loc_to_clone
        loc_to_culture = inventory.loc_to_culture
        
        # find box 
        box = _find_box(boxname, inventory)
        # error if box not found
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')

        # check if location is valid 
        _check_valid_location(box, position)
        # check if location is available for sample
        if box.samples[position[0]][position[1]]: 
            raise ValueError('Location not empty')
        
        # add sample to box's samples
        updated_samples = box.samples
        updated_samples[position[0]][position[1]] = sample
        # create updated box 
        updated_box = Box(box.name, box.description, box.loc, updated_samples)
        
        # remove old box from list of boxes (do not remove samples)
        boxes.remove(box)
        # switch out old box for new box 
        boxes.append(updated_box)

        # create new Location for sample  
        location = Location(boxname, position[0], position[1], sample.label, sample.sidelabel)
        
        # update info for inventory 
        # make new set if doens't exist 
        if sample.construct not in construct_to_locs: 
            construct_to_locs[sample.construct] = set()
        construct_to_locs[sample.construct].add(loc)
        loc_to_conc[loc] = sample.concentration
        loc_to_clone[loc] = sample.clone
        loc_to_culture[loc] = sample.culture
        
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)

    def remove_sample(position: tuple[int, int], boxname: str, inventory: Inventory):
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
        box = _find_box(boxname, inventory)
        # error if box not found
        if box == None: 
            raise ValueError(f'Box: {boxname} does not exist in inventory')
        
        # check if location is valid 
        _check_valid_location(box, position)
        # check if location contains a sample
        if box.samples[position[0]][position[1]] == None: 
            raise ValueError('Location is empty')
            
        # remove sample from box's samples
        updated_samples = box.samples
        updated_samples[position[0]][position[1]] = None
        # create updated box 
        updated_box = Box(box.name, box.description, box.loc, updated_samples)
        
        # remove old box from list of boxes (do not remove samples)
        boxes.remove(box)
        # update box
        boxes.append(updated_box)
        
        # define sample location 
        loc = Location(boxname=box.name, row=i, col=j, 
                    label=sample.label, sidelabel=sample.sidelabel)
        # remove sample info from inventory
        construct_to_locs[sample.construct].remove(loc)
        del loc_to_conc[loc] 
        del loc_to_clone[loc] 
        del loc_to_culture[loc]
        
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)  
    
    def find_sample(query: dict, inventory: Inventory) -> List[Location]: 
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

        for box in inventory.boxes:
            for row_idx, row in enumerate(box.samples):
                for col_idx, sample in enumerate(row):
                    if not sample:
                        continue

                    if all(getattr(sample, key, None) == value for key, value in query.items()):
                        location = Location(
                            boxname=box.name,
                            row=row_idx,
                            col=col_idx,
                            label=sample.label,
                            sidelabel=sample.sidelabel
                        )
                        matches.add(location)

        return list(matches) 

    def add_box(box: Box, inventory: Inventory) -> Inventory:
        '''
        Add box to inventory
        
        Args: 
        box (Box): Box instance to add to inventory 
        inventory (Inventory): Inventory instance to add box to 
        
        Returns: 
        Inventory: Updated Inventory instance with box added 
        
        '''
        # values of new inventory
        boxes = inventory.boxes
        construct_to_locs = inventory.construct_to_locations
        loc_to_conc = inventory.loc_to_conc
        loc_to_clone = inventory.loc_to_clone
        loc_to_culture = inventory.loc_to_culture

        # check that box with same name does not already exist 
        if _find_box(box.name, inventory):
            raise ValueError(f'Box with name {boxname} already exist in inventory')

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
    
    def remove_box(boxname: str, inventory: Inventory) -> Inventory:
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
        box = _find_box(boxname, inventory)
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
                    del loc_to_conc[loc] 
                    del loc_to_clone[loc] 
                    del loc_to_culture[loc]
                    
        # remove box 
        boxes.remove(box)
        
        # return new inventory with updated info 
        return Inventory(boxes, construct_to_locs, loc_to_conc, loc_to_clone, loc_to_culture)

    def update_box(boxname, updates, inventory) -> Inventory: 
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
        box = _find_box(boxname, inventory)
        
        # Update fields with new values or keep existing values
        name = updates.get('name', box.name)
        description = updates.get('description', box.description)
        location = updates.get('location', box.location)
        
        # Create the updated box
        updated_box = Box(name, description, location, box.samples)

        # If the name was changed, update sample locations
        if name != box.name:
            # Remove the old box
            inventory = remove_box(box, inventory)
            # Add the updated box to the inventory
            return add_box(updated_box, inventory)
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

    def retrieve_box_contents(boxname: str, inventory: Inventory):
        '''
        Retrieves contents of specified box
        
        Args: 
        boxname (str): Name of box whose contents are to be retrieved
        inventory (Inventory): Current inventory 
        
        Return:
        List[List[Sample]]: Content of specified box structured as 
        2D array corresponding to layout of box
        '''
        box = _find_box(boxname, inventory)
        return box.samples

    # HELPER FUNC
    def _find_box(boxname: str, inventory: Inventory) -> Box: 
        '''
        Finds box in inventory with given name

        Args: 
        boxname (str): name of box to search for 
        inventory (Inventory): inventory to seach for box for

        Returns: 
        Box: box with boxname or None if no box found
        '''
        for box in in inventory.boxes: 
            if box.name == boxname: 
                return box   
        return None

    # HELPER FUNC
    def _check_valid_location(box: Box, position: Tuple[int, int]): 
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



    





