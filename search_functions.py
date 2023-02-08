import misc_functions
from tabulate import tabulate # For printing results in user readable format

def fetch_book_details(cursor, return_to_main_menu, custom_action):
    '''
    This function allows a user to fetch the details of an existing book based on its ID or Title.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
        custom_action (str): Used to customise user prompts on console for UI and readability purposes
    '''
    # Prompts user whether they want to search by book ID or Title, using while-except block to restrict user entry
    while True:
        try:
            print("Type:\n—\'ID\' to search for a book by its id.\n—\'TITLE\' to search for a book by its title\n—\'MENU\' to return to the main menu")
            book_search_method = input("").upper().strip()
            if book_search_method not in ['ID', 'TITLE', 'MENU']:
                raise ValueError
            break
        except ValueError:
            print("ERROR: Invalid input. Please only enter \'ID\', \'TITLE\' or \'MENU\'.")
    # Search for a book by ID
    if book_search_method == 'ID':
        while True:
            try:
                book_id = int(input(f"Enter the id of the book you wish to {custom_action}:\n"))
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
        book_details_dicts = fetch_book_details_by_id(cursor, book_id)
        return book_details_dicts
    # Search for a book by Title
    elif book_search_method == 'TITLE':
        book_title = input(f"Enter the title of the book you wish to {custom_action}:\n").strip()
        book_details_dicts = fetch_book_details_by_title(cursor, book_title)
        return book_details_dicts
    # Return to the main menu
    elif book_search_method == 'MENU':
        return_to_main_menu()

def fetch_book_details_by_id(cursor, book_id):
    '''
    This function allows a user to fetch the details of an existing book based on its ID.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        book_id (int): Book ID that is checked
    '''
    # Used to store the ID, Title, Author and Qty once they have passed the right checks
    book_details_dict = {'id': None, 'Title': None, 'Author': None, 'Qty': None}
    # Checks if user-entered Book ID already exists and prompts user to re-enter if so
    existing_id_flag = misc_functions.check_book_id_exists(cursor, book_id)
    # If book ID does not exist
    if existing_id_flag == 0:
        print(f"ERROR: Book ID {book_id} does not exist.")
    # If the book ID already exists, fetch details of the book
    elif existing_id_flag == 1:
        # Fetch the book details based on the ID and update the book details dictionary
        cursor.execute(f"SELECT id, Title, Author, Qty FROM books WHERE id = {book_id};")
        book_details_list = cursor.fetchone()
        book_details_dict['id'] = book_details_list[0]
        book_details_dict['Title']  = book_details_list[1]
        book_details_dict['Author']  = book_details_list[2]
        book_details_dict['Qty']  = book_details_list[3]
        # Print the book details to the user
        print(f"Here are the book details for book id {book_id}:")
        book_details_headers = book_details_dict.keys()
        book_details_data = [book_details_dict.values()]
        print(tabulate(book_details_data, headers=book_details_headers, tablefmt="simple_outline"))
    # Allows for manipulation of fetched book elsewhere (i.e. updating or deleting)
    book_details_dicts = [book_details_dict]
    return book_details_dicts

def fetch_book_details_by_title(cursor, book_title):
    '''
    This function allows a user to fetch the details of an existing book based on its title.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        book_title (str): Book title that is checked
    '''
    # Used to store the ID, Title, Author and Qty once they have passed the right checks
    book_details_dict = {'id': None, 'Title': None, 'Author': None, 'Qty': None}
    # Fetch entries for a given book title
    cursor.execute(f"SELECT id, Title, Author, Qty FROM books WHERE Title = '{book_title}';")
    book_details_list = cursor.fetchall()
    book_count = len(book_details_list)
    # Converts result from list of tuples to list of lists using list comprehension
    book_details_data = [list(tup) for tup in book_details_list]
    if book_count != 0:
        # Print the book details to the user
        print(f"{book_count} entry(s) found for book title \'{book_title}\':")
        book_details_headers = book_details_dict.keys()
        print(tabulate(book_details_data, headers=book_details_headers, tablefmt="simple_outline"))
        # Create a list of dictionaries containing the values (for use elsehwere in delete func)
        book_details_dicts = []
        for book in book_details_data:
            book_details_dicts.append({'id': book[0], 'Title': book[1], 'Author': book[2], 'Qty': book[3]})
        return book_details_dicts
    else:
        print(f"No entries found for book title \'{book_title}\'")
        book_details_dicts = [book_details_dict]
        return book_details_dicts

def search_again_or_go_to_menu(cursor, return_to_main_menu, custom_action):
    '''
    This function allows a user to search for another book or return to the main menu.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
        custom_action (str): Used to customise user prompts on console for UI and readability purposes
    '''
    # Ask user if they wish to search again or return to main menu
    while True:
        try:
            print("Do you wish to add search for another book or return to the main menu?\nType:")
            print("—\'Y\' to search for a new book.\n—\'N\' to return to the main menu.")
            new_book_id_or_menu_reply = input().upper().strip()
            # Execute decision logic based on user reply
            if new_book_id_or_menu_reply == 'Y':
                fetch_book_details(cursor, return_to_main_menu, custom_action)
            elif new_book_id_or_menu_reply == 'N':
                break
        except ValueError:
            print("Invalid input. Please enter only \'Y\' or \'N\'.")
    return_to_main_menu()
