import misc_functions
import search_functions
from tabulate import tabulate # For printing results in user readable format

def update_book(book_to_be_updated, cursor, return_to_main_menu):
    '''
    This function allows a user to update a book from the database.

    Args:
        book_to_be_updated (dict): dict containing the details of the book to be updated
        cursor (str): Used to customise user prompts on console for UI and readability purposes
        return_to_main_menu (str): imports return_to_main_menu function from main.py
    '''

    if book_to_be_updated['id'] == None:
        return_to_main_menu()
    else:
        # Ask user if they wish to update the book they have fetched
        while True:
            try:
                print(f"Are you sure you wish to update \'{book_to_be_updated['Title']}\' by \'{book_to_be_updated['Author']}\' (id: {book_to_be_updated['id']}) in the database?\nType:")
                print("—\'Y\' to update this book.\n—\'N\' to return to the main menu.")
                update_confirmation_reply = input().upper().strip()
                if update_confirmation_reply not in ['Y', 'N']:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid input (\'Y\' or \'N\') only.")
        print("—"*90,f"\nUPDATING: \'{book_to_be_updated['Title'].upper()}\' BY \'{book_to_be_updated['Author'].upper()}\' (ID: {book_to_be_updated['id']}):")
        # Execute decision logic based on user reply
        if update_confirmation_reply == 'Y':
            # Ask user which field they then wish to update
            while True:
                try:
                    print(f"Enter which field you wish to update for \'{book_to_be_updated['Title']}\' by \'{book_to_be_updated['Author']}\' (id: {book_to_be_updated['id']}). \nType:")
                    print("—\'ID\' to update the ID.\n—\'TITLE\' to update the book title.\n—\'AUTHOR\' to update the book author.\n—\'QTY\' to update the book quantity.\n—\'MENU\' to return to the main menu.")
                    field_to_update = input().upper().strip()
                    if field_to_update not in ['ID', 'TITLE', 'AUTHOR', 'QTY', 'MENU']:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid field.")
            # Execute update field function
            if field_to_update != 'MENU':
                update_field(book_to_be_updated, field_to_update, book_to_be_updated['id'], cursor, return_to_main_menu)
            else:
                return_to_main_menu()
        # Return to main menu if the user didn't want to update the book
        elif update_confirmation_reply == 'N':
            return_to_main_menu()
            
def update_field(book_to_be_updated, field_name, book_id, cursor, return_to_main_menu):
    '''
    This function allows a user to update a specific field by id.

    Args:
        book_to_be_updated (dict): dictionary containing the details of the book as key-value pairs
        field_name (str): the name of the field to be updated
        book_id (int): the id of the book to be updated
        cursor (str): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
    '''

    # Fetch the old value of the field
    cursor.execute(f"SELECT {field_name} FROM books WHERE id = {book_id};")
    old_value = cursor.fetchone()[0]
    print(f"The value of \'{field_name}\' for \'{book_to_be_updated['Title']}\' by \'{book_to_be_updated['Author']}\' (id: {book_to_be_updated['id']}) is currently set to \'{old_value}\'.")
    # Ask user if they wish to update this field
    while True:
        try:
            print(f"Would you like to update this field? Type:")
            print(f"—\'Y\' to update this value\n—\'N\' to update another field or return to the main menu.")
            update_field_confirm = input().upper().strip()
            if update_field_confirm not in ['Y', 'N']:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a valid option (only \'Y\' or \'N\').")

    # Execute decision logic based on user reply
    print("—"*90,f"\nUPDATING: \'{field_name}\'")
    if update_field_confirm == 'Y':
        while True:
            try:
                new_value = input(f"Enter the new value of \'{field_name}\' for \'{book_to_be_updated['Title']}\' by \'{book_to_be_updated['Author']}\' (ID: {book_id}):\n").strip()
                # QA Check: prevent entry of existing ID already or non-numeric id values
                if field_name == 'ID':
                    quality_assurance_criteria_met = prevent_non_numerics(new_value)
                    quality_assurance_criteria_met = prevent_duplicate_existing_id(new_value, cursor)
                    break
                # QA Check: prevent entry of duplicate author-title combination
                if field_name == 'TITLE' or field_name == 'AUTHOR':
                    quality_assurance_criteria_met = prevent_existing_title_author_combination(field_name, new_value, book_to_be_updated, cursor)
                    break
                # QA Check: prevent entry of non-numeric id values for quantity
                if field_name == 'QTY':
                    quality_assurance_criteria_met = prevent_non_numerics(new_value)
                    break
            except ValueError as error:
                print(error)
        # Update the value only once all QA checks have been passed else return to main menu
        if quality_assurance_criteria_met == True:
            cursor.execute(f"UPDATE books SET {field_name} = \"{new_value}\" WHERE id = {book_id};")
            print(f"The value of \'{field_name}\' for \'{book_to_be_updated['Title']}\' by \'{book_to_be_updated['Author']}\' (ID: {book_to_be_updated['id']}) has been successfully updated from \'{old_value}\' to \'{new_value}\'.")
        elif quality_assurance_criteria_met == False:
            return_to_main_menu()

def update_another_book(cursor, return_to_main_menu):
    '''
    This function allows a user to update another book or return to the main menu.

    Args:
        cursor (str): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
    '''
    # Ask user if they wish to search again or return to main menu
    while True:
        try:
            print("Do you wish to update another book or return to the main menu?\nType:")
            print("—\'Y\' to search for a new book.\n—\'N\' to return to the main menu.")
            update_another_reply = input().upper().strip()
            # Execute decision logic based on user reply
            if update_another_reply == 'Y':
                # Fetch the book details of the book to be deleted
                custom_action = "update"
                book_to_be_updated = search_functions.fetch_book_details(cursor, return_to_main_menu, custom_action)[0]
                update_book(book_to_be_updated, cursor, return_to_main_menu)
            elif update_another_reply == 'N':
                break
        except ValueError:
            print("Invalid input. Please enter only \'Y\' or \'N\'.")
    return_to_main_menu()

def prevent_non_numerics(new_value):
    '''
    This function prevents a user from updating a numeric field (id, qty) with non-numeric values.

    Args:
        new_value (str): the new field value to be checked
    '''
    # Check if the input is numeric (intended for only ID or Quantity values)
    if not new_value.isnumeric():
        quality_assurance_criteria_met = False
        raise ValueError("ERROR: Non-numeric values not permitted. Please enter a numeric value only.")
    else:
        quality_assurance_criteria_met = True
    return quality_assurance_criteria_met

def prevent_duplicate_existing_id(book_id, cursor):
    '''
    This function prevents a user from updating a ID to an already existing id.

    Args:
        book_id (int): the id of the book to be updated
        cursor (str): passes the object used in main.py to execute SQL statements
    '''
    # Checks if user-entered ID already exists
    cursor.execute(f"SELECT COUNT(*) FROM books WHERE id = {book_id};")
    existing_id_flag = cursor.fetchone()[0]
    if existing_id_flag == 1:
        quality_assurance_criteria_met = False
        raise ValueError(f"ERROR: ID {book_id} already exists. Please enter a non-existing ID value.")
    else:
        quality_assurance_criteria_met = True
    return quality_assurance_criteria_met

def prevent_existing_title_author_combination(field_name, new_value, book_to_be_updated, cursor):
    '''
    This function prevents a user from updating a book's title or author such that the new combination of author and
    title is the same as an already existing entry. This events duplicate entries from being added.

    Args:
        field_name (str): the field to be updated
        new_value (str): the new value of the field to be updated
        book_to_be_updated (dict): dictionary containing the details of the book as key-value pairs
        cursor (str): passes the object used in main.py to execute SQL statements
    '''

    if field_name == 'TITLE':
        # Checks if user-entered book title/author combination already exists for the new value
        cursor.execute(f"SELECT COUNT(*) FROM Books WHERE Title = \"{new_value}\" AND Author = \"{book_to_be_updated['Author']}\";")
        existing_book_flag = cursor.fetchone()[0]
        # Raise an error message if the title/author combination already exists
        if existing_book_flag == 1:
            cursor.execute(f"SELECT id FROM Books WHERE Title = \"{new_value}\" AND Author = \"{book_to_be_updated['Author']}\";")
            existing_book_id = cursor.fetchone()[0]
            print(f"ERROR: \'{new_value}\' by \'{book_to_be_updated['Author']}\' already exists (ID: {existing_book_id})")
            quality_assurance_criteria_met = False
            return quality_assurance_criteria_met
        else:
            quality_assurance_criteria_met = True
            return quality_assurance_criteria_met
    elif field_name == 'AUTHOR':
        # Checks if user-entered book title/author combination already exists for the new value
        cursor.execute(f"SELECT COUNT(*) FROM Books WHERE Title = \"{book_to_be_updated['Title']}\" AND Author = \"{new_value}\";")
        existing_book_flag = cursor.fetchone()[0]
        # Raise an error message if the title/author combination already exists
        if existing_book_flag == 1:
            cursor.execute(f"SELECT id FROM Books WHERE Title = \"{book_to_be_updated['Title']}\" AND Author = \"{new_value}\";")
            existing_book_id = cursor.fetchone()[0]
            print(f"ERROR: \'{book_to_be_updated['Title']}\' by \'{new_value}\' already exists (ID: {existing_book_id})")
            quality_assurance_criteria_met = False
            return quality_assurance_criteria_met
        else:
            quality_assurance_criteria_met = True
            return quality_assurance_criteria_met
