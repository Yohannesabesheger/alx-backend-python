#!/usr/bin/python3

import seed

def main():
    # Step 1: Connect to MySQL server
    connection = seed.connect_db()
    if connection:
        seed.create_database(connection)
        connection.close()
        print("connection successful")

        # Step 2: Connect to ALX_prodev database
        connection = seed.connect_to_prodev()
        if connection:
            # Step 3: Create table
            seed.create_table(connection)
            # Step 4: Insert data from CSV
            seed.insert_data(connection, 'user_data.csv')

            # Step 5: Verify database and display first 5 rows
            cursor = connection.cursor()
            cursor.execute("""
                SELECT SCHEMA_NAME 
                FROM INFORMATION_SCHEMA.SCHEMATA 
                WHERE SCHEMA_NAME = 'ALX_prodev';
            """)
            result = cursor.fetchone()
            if result:
                print("Database ALX_prodev is present")

            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
        else:
            print("Failed to connect to ALX_prodev")
    else:
        print("Failed to connect to MySQL server")

if __name__ == '__main__':
    main()
