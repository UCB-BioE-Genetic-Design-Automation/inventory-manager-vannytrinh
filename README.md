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
# CompToDNAPy

CompToDNAPy is a Python project designed for bioengineering students to understand the process of selecting ribosome binding sites (RBS) and designing transcripts. This project follows the Function/Model pattern, separating data models from business logic.

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
   git clone https://github.com/your_username/CompToDNAPy.git
   ```
4. Change directories to enter the project:

   ```
   cd CompToDNAPy
   ```
5. Run the program:

   ```
   python3 -m comp_to_dna_py
   ```

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

## Authors

* **Your Name** - *Initial work* - [YourUsername](https://github.com/your_username)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
