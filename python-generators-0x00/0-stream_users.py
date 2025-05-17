#!/usr/bin/python3

import mysql.connector

def stream_users():
    """Generator that yields user data rows one by one as dictionaries."""
    try:
        # Connect to the ALX_prodev database
        conn = mysql.connector.connect(
            host="localhost",
            user="######",
            password="#####",  # Update this with your MySQL root password
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
