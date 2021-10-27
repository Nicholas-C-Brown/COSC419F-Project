# COSC419F-Project

## Installation
1. Ensure you have the latest version of [python](https://www.python.org/downloads/) installed.

2. Install `pipenv`
    1. Open the command terminal
    2. Run `pip install pipenv`

3. Download the project dependencies
    1. Open the command terminal in the project root directory
    2. Run `pipenv shell` to start the virtual environment
    3. Run `pipenv update` to download the project's dependencies



## Running the Application
Run `python main.py` to start the application.



## Running Unit Tests
- To run all tests run `python -m unittest discover -s <path to tests directory>` in a command terminal.

- To run a specific test file:
    - Run the test file directly `python <test_file>.py
    - Run `python -m unittest <test_file>.<TestClass>`

- To run a specific test
    - Run `python -m unittest <test_file>.<TestClass>.<test_name>`

## Running PyLint
Run `pylint <directory>` from the command terminal to run pylint on all files in the given directory.



