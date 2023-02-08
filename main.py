'''
    TASK 48: capstone_v.py
    MO EL-JARAD
'''

import sqlite3 # For using SQLite database file
from tabulate import tabulate # For printing results in user readable format
import add_functions
import search_functions
import misc_functions
import delete_functions
import update_functions

def create_database_and_connection():
    '''
    This function establishes a connection to the database file and creates a cursor object.

    Args:
        (None)
    '''
    functional_connection = sqlite3.connect("ebookstore.db") # Create and connect to a database called 'ebookstore'
    functional_cursor = functional_connection.cursor() # Create a cursor object used to execute SQL statements and retrieve results from the database
    return functional_connection, functional_cursor # Return these so they can be stored in global variables and referenced in other functions

def execute_and_commit_query(expression):
    '''
    This function execute simple SQL queries that can be stored in a string and commits these to the database file.

    Args:
        expression (string): represents the desired basic SQL query.
    '''
    global cursor # Refers to global cursor object
    cursor.execute(expression)
    conn.commit()

def print_update():
    '''
    This function presents changes to the database by printing a graphical tabular view using the Tabulate module.

    Args:
        (None)
    '''
    global cursor # Refers to global cursor object
    headers = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    tablename_local = 'books'
    print(f"Table \'{tablename_local}\' updated successfully successfully:")
    print(tabulate(data, headers=headers, tablefmt="simple_outline"))

def create_books_table():
    '''
    This function creates a table called 'books'.

    Args:
        (None)
    '''
    global cursor # Refers to global cursor object
    print("Creating new table \'books\'...")
    execute_and_commit_query("CREATE TABLE books (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)")
    execute_and_commit_query("SELECT * FROM books")
    headers = [description[0] for description in cursor.description] # Uses list comprehension to create column headers list from SQL query results
    print("Table \'books\' created successfully:")
    print(tabulate([headers], headers="firstrow", tablefmt="simple_outline"))

def initial_populate_books_table():
    global cursor # Refers to global cursor object
    global conn # Refers to global connection object
    print("Adding new rows to \'books\'...")
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (3001, 'A Tale of Two Cities', 'Charles Dickens', 30))
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40))
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25))
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37))
    cursor.execute("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", (3005, 'Alice in Wonderland', 'Lewis Carroll', 12))
    conn.commit()
    cursor.execute("SELECT * FROM books")
    conn.commit()
    print_update()

def print_main_menu():
    '''
    This function prints a menu to the user console.

    Args:
        (None)
    '''

    # Prints a user menu to the console:
    print("—"*90,"\nUSER MENU:")
    print("— \'ENTER\': Add a new book to the database.")
    print("— \'UPDATE\': Update the details of an existing book in the database.")
    print("— \'DELETE\': Delete an existing book from the database.")
    print("— \'SEARCH\': Search for an existing book in the database.")
    print("— \'EXIT\': Close the programme.")

    # Restricts user input to valid inputs
    while True:
        try:
            user_reply = input("\nEnter the corresponding word to select an option from the user menu:\n").strip().upper()
            if user_reply not in ['ENTER', 'UPDATE', 'DELETE', 'SEARCH', 'EXIT']:
                raise ValueError
            break
        except ValueError:
            print("ERROR: Invalid input. Please enter a valid selection from the menu.")

    # Allows user to add a new book
    if user_reply == 'ENTER':
        add_functions.add_new_book(cursor, return_to_main_menu, execute_and_commit_query)
    # Allows user to update a book based on its ID or title
    elif user_reply == 'UPDATE':
        # Print section title, description and border to console for UI and readability purposes
        print("—"*90,"\nUPDATE AN EXISTING BOOK IN THE DATABASE:")
        print("This feature will allow you to update a book that already exists in the \'books\' table.\n")
        # Fetch the book details of the book to be deleted
        custom_action = "update"
        book_details_dicts = search_functions.fetch_book_details(cursor, return_to_main_menu, custom_action)
        # Fetches book to be updated based on user selection of ID or Title
        if len(book_details_dicts) == 1: # Effectively if ID is selected or if only one title exists
            book_to_be_updated = book_details_dicts[0]
        elif len(book_details_dicts) > 1: # Effectively if more than one book exists with the same title
            # Restrict numeric ID entry only
            while True:
                try:
                    book_id_to_be_updated = int(input(f"More than one book found.\nEnter the id of the book you wish to update:\n"))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            # Retrieve book details of the book to be deleted based on the entered ID
            book_details_dicts = search_functions.fetch_book_details_by_id(cursor, book_id_to_be_updated)
            book_to_be_updated = book_details_dicts[0]
        # Execute update functions
        update_functions.update_book(book_to_be_updated, cursor, return_to_main_menu)
        update_functions.update_another_book(cursor, return_to_main_menu)
    # Allows user to search for a book based on its ID or title
    elif user_reply == 'SEARCH':
        # Used to customise user prompts on console for UI and readability purposes
        custom_action = "search for"
        # Print section title, description and border to console for UI and readability purposes
        print("—"*90,"\nSEARCH FOR AN EXISTING BOOK IN THE DATABASE:")
        print("This feature will allow you to search for a book that already exists in the \'books\' table.\n")
        print("Begin by selecting whether you wish to search for a book by id or Title:")
        # Fetch the book details
        search_functions.fetch_book_details(cursor, return_to_main_menu, custom_action)
        search_functions.search_again_or_go_to_menu(cursor, return_to_main_menu, custom_action)
    # Allows user to delete a book based on its ID or title
    elif user_reply == 'DELETE':
        # Print section title, description and border to console for UI and readability purposes
        print("—"*90,"\nDELETE AN EXISTING BOOK IN THE DATABASE:")
        print("This feature will allow you to delete a book that already exists in the \'books\' table.\n")
        # Fetch the book details of the book to be deleted
        custom_action = "delete"
        book_details_dicts = search_functions.fetch_book_details(cursor, return_to_main_menu, custom_action)
        # Fetch book to be deleted based on user selection of ID or Title
        if len(book_details_dicts) == 1: # Effectively if ID is selected or if only one title exists
            book_to_be_deleted = book_details_dicts[0]
        elif len(book_details_dicts) > 1: # Effectively if more than one book exists with the same title
            # Restrict numeric ID entry only
            while True:
                try:
                    book_id_to_be_deleted = int(input(f"ERROR: More than one book found.\nEnter the id of the book you wish to delete:\n"))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            # Retrieve book details of the book to be deleted based on the entered ID
            book_to_be_deleted = search_functions.fetch_book_details_by_id(cursor, book_id_to_be_deleted)[0]
        # Execute delete functions
        delete_functions.delete_book(book_to_be_deleted, cursor, return_to_main_menu)
        delete_functions.delete_another_book(cursor, return_to_main_menu)
    # Allows user to exit the program
    elif user_reply == 'EXIT':
        exit_program()

def close_connection():
    '''
    This function closes the connection to the database file.

    Args:
        (None)
    '''
    global conn
    print("Closing connection...")
    conn.close()
    print("Connection successfully terminated.")

def return_to_main_menu():
    '''
    This function is used to exit a function and go to the main menu, used at the end of decision logic.

    Args:
        (None)
    '''
    print("Returning to main menu...")
    print_main_menu()

def exit_program():
    '''
    This function is used to exit the program.

    Args:
        (None)
    '''
    # Closes the database and ends the program
    close_connection()
    quit()

print("TASK 48 - CAPSTONE PROJECT V\n")
# Establishing connection to the database and create cursor object by establishing a connection
conn = create_database_and_connection()[0]
cursor = create_database_and_connection()[1]
print("Connection to database \"ebookstore\" established successfully.")

# Create books table and populate it with data
create_books_table()
initial_populate_books_table()

# Initial prompt for user to select from main menu
print_main_menu()

# Close the connection to the database
# close_connection()
