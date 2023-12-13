# Testing Notes 
Below, I describe what main things I tested for each function in this project. This does not include Tests for the Box model methods. 

All tests can be found at [tests](tests)

## add_sample
`add_sample`
- Add one sample to a box 
  - Check that sample was added to box
  - Check that sample information in inventory is correct
- Add sample to occupied location
  - Check for error 
- Add sample to invalid location
  - Check for error
- Add multiple samples
  - Check that all information is correctly stored in inventory 

## make_box
`make_box`
- Create a 8x8 box 
  - Check that all features of box is stored correctly 
  - Check the number of rows in the box
  - Check the number of columns in the box 

## add_box
`add_box`
- Add box to inventory 
  - Check that box is now in inventory 
- Add box with same name as existing box 
  - Check for error 
- Add something that is not a box 
  - Check for error
- Add multiple boxes 
  - Check that all boxes are in inventory 

## remove_box
`remove_box`
- Remove box (box has a sample inside)
  - Check that box is removed from inventory 
  - Check that sample is removed from inventory 
- Remove a box that doesn’t exist 
  - Check for error 

## remove_sample
`remove_sample`
- Remove sample from box 
  - Check that sample removed from box 
  - Check that sample info removed from inventory 
- Remove sample at empty location 
  - Check for error 
- Remove sample at invalid location
  - Check for error 
- Remove sample from invalid box 
  - Check for error

## find_sample
`find_sample`
- Find sample w/ all fields specified in query (one matching)
  - Check for correct location for sample that match
- Find samples w/ one field specified in query 
  - Check for correct locations for samples that match
- Find samples w/ two fields specified in query 
  - Check for correct locations for samples that match
- Find samples w/ a query that matches nothing in existing inventory 
  - Check for empty list 
- Find samples w/ a query with an invalid key
  - Check for error

## update_box
`update_box`
- Update box (including name)
  - Check updated box fields are correct 
  - Check that sample locations in inventory reflect update
- Update box w/ invalid key 
  - Check for error 
- Update box that doesn’t exist
  - Check for error

## retrieve_box
`retrieve_box`
- Retrieve 8x8 box with 6 samples
  - Check for a 8x8 2d array 
  - Check for 6 samples in box 
- Retrieve box that doesn’t exists 
  - Check for error 

## tsv_to_box
`tsv_to_box` 
- Convert an example tsv file
  - Check for box with correct number of samples
- Convert an invalid filepath
  - Check for error

## box_to_tsv
`box_to_tsv`
- Convert a box to tsv 
  - Check that filepath name was correctly returned 
  - Check that box instance is unchanged 
  - Convert back from file to box and check that the boxes are equivalent 
- Convert something that is not a box
  - Check for error
