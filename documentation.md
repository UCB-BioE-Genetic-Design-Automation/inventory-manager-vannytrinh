# Methods for Updating Inventory
Methods for updating the inventory with adding/removing a box or sample

## add_sample
``` python
add_sample(sample, position, boxname, inventory)
```

Adds a new sample to a specified location in a box and updates the inventory.

### Parameters:
- sample (Sample): Sample to add
- position (tuple[int, int]): Row and column position of box to add sample to 
- boxname (str): Name of box to add sample to 
- inventory (Inventory): Current inventory 
        
### Returns
- Inventory: Updated inventory with sample added 

## remove_sample
``` python
remove_sample(position, boxname, inventory)
```

Removes a sample from a specified location in a box and updates the inventory.

### Parameters:
- position (tuple[int, int]): Row and column position of box where sample is to be removed
- boxname (str): Name of box to remove sample from
- inventory (Inventory): Current inventory 
        
### Returns
- Inventory: Updated inventory with sample removed 

## add_box
``` python
add_box
```
Adds a new box to the inventory.

### Parameters:
- box (Box): Box to add to inventory
- inventory (Inventory): Current inventory 

### Returns
- Inventory: Updated inventory with box added
  
## remove_box
``` python
remove_box
```
Removes a specified box from the inventory.

### Parameters:
- boxname (str): Name of box to remove from inventory
- inventory (Inventory): Current inventory 

### Returns
- Inventory: Updated inventory with box removed 

## update_box
``` python
update_box
```
Updates specified metadata fields of a box within the inventory and reflects these changes in the inventory.

### Parameters:
- boxname (str): Name of box to add sample to 
- inventory (Inventory): Current inventory 

### Returns
- Inventory: Updated inventory with updated box

# Methods for searching within the inventory
Methods to search an inventory for samples or retrieve the contents of a box

## find_sample
``` python
find_sample
```
Finds the locations of samples matching the given criteria within the inventory.

## retrieve_box_contents
``` python
retrieve_box_contents
```
Retrieves the contents of a specified box.

# Methods to serialize/deserialize a box
Methods to save a box as a TSV or parse a TSV into a box object

## box_to_tsv
``` python
box_to_tsv
```
Converts the data of a specified box into TSV format and saves it to a file.

## tsv_to_box
``` python
tsv_to_box
```
Converts data from a TSV (Tab-Separated Values) file into a Box object.

# Other Methods 

## make_empty_box
``` python
make_empty_box
```
Create an empty box of the given size 
