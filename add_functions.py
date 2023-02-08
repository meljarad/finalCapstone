from tabulate import tabulate # For printing results in user readable format

def add_new_book(cursor, return_to_main_menu, execute_and_commit_query):
    '''
    This function allows a user to enter a new book to the 'books' database by prompting them to enter details about
    the new book they wish to add. This function utilises a series of QA checks to prevent duplicates by ensuring
    that they cannot add an existing book, by checking for an existing ID or combination of Author & Title.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        return_to_main_menu (str): imports return_to_main_menu function from main.py
        execute_and_commit_query (str): imports execute_and_commit_query function from main.py
    '''
    # Print section title, description and border to console for UI and readability purposes
    print("—"*90,"\nADD A NEW BOOK TO THE DATABASE:")
    print("This feature will allow you to enter a new book to the \'books\' table.\n")
    # Used to store the ID, Title, Author and Qty once they have passed the right checks
    new_book_details_dict = {'id': None, 'Title': None, 'Author': None, 'Qty': None}

    # Asks user to enter the new book ID
    while True:
        try:
            new_book_id = int(input("Enter the new book ID:\n"))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Checks if user-entered Book ID already exists and prompts user to re-enter if so
    cursor.execute(f"SELECT COUNT(*) FROM books WHERE id = {new_book_id};")
    existing_id_flag = cursor.fetchone()[0]
    if existing_id_flag == 0:
        new_book_details_dict['id'] = new_book_id
        # Asks user to enter the new book title and author
        new_book_title = input("Enter the new book title:\n").strip()
        new_book_details_dict['Title'] = new_book_title
        new_book_author = input("Enter the new book author:\n").strip()

        # Checks if user-entered book Title by the same Author already exists
        cursor.execute(f"SELECT id FROM books WHERE Title = '{new_book_title}' AND Author = '{new_book_author}' ;")
        existing_book_title_by_author_flag = cursor.fetchone()

        if existing_book_title_by_author_flag:
            existing_book_id = existing_book_title_by_author_flag[0]
            print(f"ERROR: A book called '{new_book_title}' by '{new_book_author}' already exists (id = {existing_book_id}).")
            print("To update details for this book, return to the main menu and use the UPDATE function.")
            return_to_main_menu()
        else:
            new_book_details_dict['Title'] = new_book_title
            new_book_details_dict['Author'] = new_book_author
            # Asks user to enter the new book quantity
            while True:
                try:
                    new_book_qty = int(input("Enter the new book quantity:\n"))
                    new_book_details_dict['Qty'] = new_book_qty
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")

            # Print details to user for confirmation:
            print("Please confirm the following details to be added:")
            new_book_details_headers = new_book_details_dict.keys()
            new_book_details_data = [new_book_details_dict.values()]
            print(tabulate(new_book_details_data, headers=new_book_details_headers, tablefmt="simple_outline"))
            # Restricts user input to either 'Y', 'N' or 'QUIT'
            while True:
                try:
                    confirm_reply = input("Do you wish to enter these details?\nType:\n\'Y\' to add these to the Books database\n\'N\' to re-enter the new book details\n\'MENU\' to discard and return to the main menu\n").upper().strip()
                    if confirm_reply not in ['Y', 'N', 'MENU']:
                        raise ValueError
                    break
                except ValueError:
                    print("ERROR: Invalid input. Please enter 'Y', 'N', or 'QUIT'.")

            # Execute decision logic based on user input
            if confirm_reply == 'Y':
                # Insert new book details to the 'books' table
                execute_and_commit_query(f'INSERT INTO books (id, Title, Author, Qty) VALUES ({new_book_details_dict["id"]}, "{new_book_details_dict["Title"]}", "{new_book_details_dict["Author"]}", {new_book_details_dict["Qty"]});')
                # Run a SELECT query on the same details to show user it was successful
                cursor.execute((f'SELECT id, Title, Author, Qty FROM books WHERE id={new_book_details_dict["id"]} AND Title="{new_book_details_dict["Title"]}" AND Author="{new_book_details_dict["Author"]}" AND Qty={new_book_details_dict["Qty"]}'))
                confirmation_fetch_data = cursor.fetchall()
                headers = new_book_details_dict.keys()
                tablename_local = 'books'
                # Print a confirmation message to the user notifying them of the update
                print(f"Table \'{tablename_local}\' updated successfully successfully with the following new book details:")
                print(tabulate(confirmation_fetch_data, headers=headers, tablefmt="simple_outline"))
                return_to_main_menu()
            elif confirm_reply == 'N':
                add_new_book(cursor, return_to_main_menu, execute_and_commit_query)
            elif confirm_reply == 'MENU':
                return_to_main_menu()
    # If the book ID already exists, prompt user for re-entry or allow return to main menu
    elif existing_id_flag == 1:
        while True:
            try:
                print(f"ERROR: Book ID {new_book_id} already exists.")
                print("Do you wish to add another book ID or return to the main menu?\nType:")
                print("\'Y\' to add a new book.\n\'N\' to return to the main menu.")
                new_book_id_or_menu_reply = input().upper().strip()
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
        # Execute decision logic based on user reply
        if new_book_id_or_menu_reply == 'Y':
            add_new_book(cursor, return_to_main_menu, execute_and_commit_query)
        elif new_book_id_or_menu_reply == 'N':
            return_to_main_menu()
