#!/usr/bin/python3
"""
Memory-efficient average age calculation using generators.
"""

from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    Yields:
        int: The age of a user.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def average_age():
    """
    Calculates and prints the average age of all users using a generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")


# Run the function if this script is executed
if __name__ == "__main__":
    average_age()
