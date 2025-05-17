#!/usr/bin/python3
"""
Module for lazy loading user data from a database using pagination and generators.
"""

from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.

    Args:
        page_size (int): Number of users per page.
        offset (int): Starting point in the dataset.

    Returns:
        list of dicts: A page of user records.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches user data page by page.

    Args:
        page_size (int): Number of records per page.

    Yields:
        list of dicts: A page of user records.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
