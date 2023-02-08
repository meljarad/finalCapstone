import misc_functions
import search_functions
from tabulate import tabulate # For printing results in user readable format

def delete_book(book_to_be_deleted, cursor, return_to_main_menu):
    '''
    This function allows a user to delete a book from the database.

    Args:
        book_to_be_deleted (dict): dict containing the details of the book to be deleted
        cursor (str): Used to customise user prompts on console for UI and readability purposes
        return_to_main_menu (str): imports return_to_main_menu function from main.py
    '''

    if book_to_be_deleted['id'] == None:
        return_to_main_menu()
    else:
        # Ask user if they wish to delete the book they have fetched
        while True:
            try:
                print(f"Are you sure you wish to delete \'{book_to_be_deleted['Title']}\' by \'{book_to_be_deleted['Author']}\' (id: {book_to_be_deleted['id']}) from the database?\nType:")
                print("—\'Y\' to delete forever.\n—\'N\' to return to the main menu.")
                deletion_confirmation_reply = input().upper().strip()
                if deletion_confirmation_reply not in ['Y', 'N']:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid input (\'Y\' or \'N\') only.")
        # Execute decision logic based on user reply
        if deletion_confirmation_reply == 'Y':
            cursor.execute(f"DELETE FROM books WHERE id = {book_to_be_deleted['id']};")
            print(f"\'{book_to_be_deleted['Title']}\' by \'{book_to_be_deleted['Author']}\' (id: {book_to_be_deleted['id']}) has been deleted from the Books table.")
        elif deletion_confirmation_reply == 'N':
            return_to_main_menu()

def delete_another_book(cursor, return_to_main_menu):
    '''
    This function allows a user to delete another book or return to the main menu.

    Args:
        cursor (str): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
    '''
    # Ask user if they wish to search again or return to main menu
    while True:
        try:
            print("Do you wish to delete another book or return to the main menu?\nType:")
            print("—\'Y\' to search for a new book.\n—\'N\' to return to the main menu.")
            delete_another_reply = input().upper().strip()
            # Execute decision logic based on user reply
            if delete_another_reply == 'Y':
                # Fetch the book details of the book to be deleted
                custom_action = "delete"
                book_to_be_deleted = search_functions.fetch_book_details(cursor, return_to_main_menu, custom_action)[0]
                delete_book(book_to_be_deleted, cursor, return_to_main_menu)
            elif delete_another_reply == 'N':
                break
        except ValueError:
            print("Invalid input. Please enter only \'Y\' or \'N\'.")
    return_to_main_menu()
