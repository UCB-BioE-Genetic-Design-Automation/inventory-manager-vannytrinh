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
- create a 8x8 box 
  - check that all features of box is stored correctly 
  - check the number of rows in the box
  - check the number of columns in the box 

## add_box
`add_box`
- add box to inventory 
  - check that box is now in inventory 
- add box with same name as existing box 
  - check for error 
- add something that is not a box 
  - check for error
- add multiple boxes 
  - check that all boxes are in inventory 

## remove_box
`remove_box`
- remove box (box has a sample inside)
  - check that box is removed from inventory 
  - check that sample is removed from inventory 
- remove a box that doesn’t exist 
  - check for error 

## remove_sample
`remove_sample`
- remove sample from box 
  - check that sample removed from box 
  - check that sample info removed from inventory 
- remove sample at empty location 
  - check for error 
- remove sample at invalid location
  - check for error 
- remove sample from invalid box 
  - check for error

## find_sample
`find_sample`
- find sample w/ all fields specified in query (one matching)
  - check for correct location for sample that match
- find samples w/ one field specified in query 
  - check for correct locations for samples that match
- find samples w/ two fields specified in query 
  - check for correct locations for samples that match
- find samples w/ a query that matches nothing in existing inventory 
  - check for empty list 
- find samples w/ a query with an invalid key
  - check for error

## update_box
`update_box`
- update box (including name)
  - check updated box fields are correct 
  - check that sample locations in inventory reflect update
- update box w/ invalid key 
  - check for error 
- update box that doesn’t exist
  - check for error

## retrieve_box
`retrieve_box`
- retrieve 8x8 box with 6 samples
  - check for a 8x8 2d array 
  - check for 6 samples in box 
- retrieve box that doesn’t exists 
  - check for error 

## tsv_to_box
`tsv_to_box` 
- convert an example tsv file
  - check for box with correct number of samples
- convert an invalid filepath
  - check for error

## box_to_tsv
`box_to_tsv`
- convert a box to tsv 
  - check that filepath name was correctly returned 
  - check that box instance is unchanged 
  - convert back from file to box and check that the boxes are equivalent 
- convert something that is not a box
  - check for error
