import sqlite3
import functools
import datetime
from datetime import datetime

# decorator to lof SQL queries

""" YOUR CODE GOES HERE"""


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")


def log_queries(func):
    """
    Decorator to log SQL queries executed by the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]
        print(f"Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper


# Example usage
# Create a sample SQLite database and table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')
