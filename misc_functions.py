def check_book_id_exists(cursor, book_id):
    '''
    This function allows a user to check if a book ID already exists.

    Args:
        cursor (string): passes the object used in main.py to execute SQL statements
        book_id (int): Book ID that is checked
    '''
    # Checks if user-entered Book ID already exists and prompts user to re-enter if so
    cursor.execute(f"SELECT COUNT(*) FROM books WHERE id = {book_id};")
    existing_id_flag = cursor.fetchone()[0]
    return existing_id_flag
