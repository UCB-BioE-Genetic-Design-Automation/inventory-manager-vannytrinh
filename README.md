# InventoryManager

InventoryManager is a Python project designed to organize and track DNA samples within a laboratory environment. This project follows the Function/Model pattern, separating data models from business logic.

## Purpose

InventoryManager manages DNA samples such as plasmid sequences, oligos, and purified PCR products and their locations in the lab. The system stores samples and their data, such as the labels on their tubes, their concentration, construct, and more. The samples are stored in boxes, which are all stored in an inventory. Quickly search for a sample's location based on their properties or retrieve all samples in a box. Efficiently update the inventory by adding/removing samples or adding/removing/updating boxes. You can also convert between a box object and TSV file (Examples of TSV input/output files are located at [tests/data](tests/data)). 

More information about the capabilities and functions of InventoryManager can be found in [documentation.md](documentation.md).

## Testing

Tests for the project can be found in the tests file. Multiple functions are tested (and passed)! They include:
- Adding a new (empty) box to the inventory
- Adding samples to the box
- Looking for specific samples of given properties
- Removing a sample
- Removing a box
- Updating a box with new information
- Turning a box into a TSV
- Reading a TSV into a box

There are a total of 12 tests(10 InventoryModel, 2 Box), one for each existing method. Tests can be found at [tests/test_inventory_manager](tests/inventory-manager.py) and information on what the tests do can be found at [testing.md](testing.md).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python installed on your machine. If you don't have Python, let's install it first.

#### Installing Python

1. Download Python from the official [Python website](https://www.python.org/downloads/).
2. Run the installer and follow the on-screen instructions. Make sure to check the box that says "Add Python to PATH" before you click "Install Now".

### Running the Program

1. Open your command prompt (cmd) or terminal.
2. Navigate to the directory where you want to download this project.
3. Clone the project to your local machine:

   ```
   git clone https://github.com/vannytrinh/CompToDNAPy.git
   ```
4. Change directories to enter the project:

   ```
   cd inventory_manager_py
   ```
5. Run the program:

   ```
   python3 -m inventory_manager_py
   ```
### Setting Up a Virtual Environment and pytest

For isolation of project dependencies, it's a good practice to use a virtual environment. Here's how you can set one up:

1. Navigate to the project directory if you're not already there.

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
   ```
   venv\Scripts\activate
   ```
   - On MacOS and Linux:
   ```
   source venv/bin/activate
   ```

4. With the virtual environment activated, install the project dependencies:
   ```
   pip install -r requirements.txt
   ```

This project uses pytest for testing. If you haven't installed it yet, you can do so by running:

```
pip install pytest
```

To run tests, you can use the following command from the project directory:

```
pytest
```

This will discover tests following the pytest conventions and execute them.

To deactivate the virtual environment when you're done, simply type:

```
deactivate
```

Remember, every time you start working on the project, activate the virtual environment and deactivate it once you're done.

### Running the Tests

This project uses unittest as the testing framework. To run tests, follow these steps:

1. Navigate to the project directory if you're not already there.

2. Run the tests:

   ```
   python -m unittest discover tests
   ```

## For Complete Beginners

If this is your first time using the command line, don't worry, here are the steps you need to follow:

1. How to open your command prompt or terminal:
   - Windows: Press `Windows + R`, then type `cmd` and press `Enter`.
   - Mac: Press `Cmd + Space` to open Spotlight, then type `Terminal` and press `Enter`.
   - Linux: Press `Ctrl + Alt + T`.

2. How to navigate directories:
   - Use the command `cd your_directory_name` to enter a specific directory.
   - Use the command `cd ..` to go back one directory.

3. How to clone a GitHub project:
   - First, you need to copy the project's URL from GitHub.
   - In your terminal, type `git clone ` followed by the URL you copied.

4. How to run a Python program or tests:
   - Follow the instructions above in the "Running the Program" and "Running the Tests" sections.

Don't be afraid to explore and make mistakes. That's a huge part of the learning process!

## Future Directions
Here are some ideas I didn't have time to implement for this project but could be beneficial for a future edition!
- Identifying available position(s) to add/move a sample
- Moving a sample from one location to another
- Searching for samples that fit any queries provided (not just all queries provided)
- Expand the system to store other reagents (ex. enzymes, buffers, etc...)

## Authors

* **Van Trinh** - *Initial work* - [vannytrinh](https://github.com/vannytrinh)

## Acknowledgments

* UCB BIOE134: Genetic Design Automation with Professor J. Christoper Anderson
