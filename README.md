# Capstone Project V
This readme file will outline how to run the Python files for Capstone Project V. The project explores functions of an SQLite database called *ebookstore* used to store books in the *books* table. The core program is run from **main.py** with functions imported from the other .py files.

## Requirements and Usage
To run this code, you will need the following:

| Requirement                                  | Installation command (Mac)              | Installation command (Windows)          |
|----------------------------------------------|-----------------------------------------|-----------------------------------------|
| Python 3                                     | Already installed on your system        | Already installed on your system        |            |
| tabulate library                             | pip install tabulate                    | python -m pip install tabulate          |


## Functionality
This program includes 6 main python files:

- **main.py**: used to execute the core program and interact with the *ebookstore* database.
- **add_functions.py**: contains functions used to add new records to the database.
- **delete_functions.py**: contains functions used to remove existing records from the database.
- **search_functions.py**: contains functions used to fetch details of an individual book by searching by ID or title.
- **update_functions.py**: contains functions used to update existing records within the database.
- **misc_functions.py**: contains miscellaneous functions that may be used in **main.py**.


## Output
The script will output all findings to the console and make changes directly to the *ebookstore* database for any read/write queries. 
