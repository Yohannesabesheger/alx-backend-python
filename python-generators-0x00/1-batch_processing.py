#!/usr/bin/python3
"""
Module for batch processing users from a database using generators.
"""

import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields users from the database in batches.

    Args:
        batch_size (int): Number of records to yield per batch.

    Yields:
        list of dicts: A batch of user records.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="#####", 
            password="#######",  
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM user_data")
        total_rows = cursor.fetchone()['total']

        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            )
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return


def batch_processing(batch_size):
    """
    Processes each batch by filtering users over the age of 25.

    Args:
        batch_size (int): The size of each batch to fetch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
