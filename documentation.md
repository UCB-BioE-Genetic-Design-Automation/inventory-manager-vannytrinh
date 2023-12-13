# Methods for Updating Inventory
Methods for updating the inventory with adding/removing a box or sample

## add_sample
``` python
InventoryManager.add_sample(sample, position, boxname, inventory)
```

Adds a new sample to a specified location in a box and updates the inventory.

### Parameters
- sample (Sample): Sample to add
- position (tuple[int, int]): Row and column position of box to add sample to 
- boxname (str): Name of box to add sample to 
- inventory (Inventory): Current inventory 
        
### Return
- Inventory: Updated inventory with sample added 

## remove_sample
``` python
InventoryManager.remove_sample(position, boxname, inventory)
```

Removes a sample from a specified location in a box and updates the inventory.

### Parameters
- position (tuple[int, int]): Row and column position of box where sample is to be removed
- boxname (str): Name of box to remove sample from
- inventory (Inventory): Current inventory 
        
### Return
- Inventory: Updated inventory with sample removed 

## add_box
``` python
InventoryManager.add_box(box, inventory)
```
Adds a new box to the inventory.

### Parameters
- box (Box): Box to add to inventory
- inventory (Inventory): Current inventory 

### Return
- Inventory: Updated inventory with box added
  
## remove_box
``` python
InventoryManager.remove_box(boxname, inventory)
```
Removes a specified box from the inventory.

### Parameters
- boxname (str): Name of box to remove from inventory
- inventory (Inventory): Current inventory 

### Return
- Inventory: Updated inventory with box removed 

## update_box
``` python
InventoryManager.update_box(boxname, updates, inventory)
```
Updates specified metadata fields of a box within the inventory and reflects these changes in the inventory.

### Parameters
- boxname (str): Name of box to add sample to 
- inventory (Inventory): Current inventory 

### Return
- Inventory: Updated inventory with updated box

# Methods for Searching Within the Inventory
Methods to search an inventory for samples or retrieve the contents of a box

## find_sample
``` python
InventoryManager.find_sample(query, inventory)
```
Finds the locations of samples matching the given criteria within the inventory.

### Parameters
- query (dict): Dictionary of keys corresponding to fields of a Sample ('label', 'sidelabel', 'concentration', 'culture', 'clone')
- inventory (Inventory): Current inventory
        
### Return
- List[Location]: List of location objects for found samples

## retrieve_box_contents
``` python
InventoryManager.retrieve_box_contents(boxname, inventory)
```
Retrieves the contents of a specified box.

### Parameters
- boxname (str): Name of box whose contents are to be retrieved
- inventory (Inventory): Current inventory 
        
### Return
- List[List[Sample]]: Content of specified box structured as 2D array corresponding to layout of box

# Methods to Serialize/Deserialize a box
Methods to save a box as a TSV or parse a TSV into a box object

## box_to_tsv
``` python
InventoryManager.box_to_tsv(box, filepath)
```
Converts the data of a specified box into TSV format and saves it to a file.

### Parameters
- box (Box): Box whose data is to be converted
- filepath (str): Filepath wheer tsv is to be stored
        
### Return
- str: name of filepath where TSV was saved

## tsv_to_box
``` python
InventoryManager.tsv_to_box(filepath)
```
Converts data from a TSV (Tab-Separated Values) file into a Box object.

### Parameters
- filepath (str): Filepath of TSV to be converted
        
### Return
- Box: Box object created from TSV file

# Other InventoryManager Methods 

## make_empty_box
``` python
InventoryManager.make_empty_box(name, description, location, size)
```
Create an empty box of the given size 

### Parameters
- name (str): Name of box
- description (str): Description of box
- location (str): Location of box
- size tuple[int, int]: Number of rows and number of columns to make box

### Return
- Box: Box of given size

# Methods for Box 

## get_size
``` python
Box.get_size()
```
Get the size of the box

### Retur
- tuple[int, int]: Number of rows, number of columns

## get_num_samples
``` python
Box.get_num_samples()
```
Get the number of samples stored in the box 

### Return
- int: Number of samples
