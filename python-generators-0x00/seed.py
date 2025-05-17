import mysql.connector
import csv
import uuid

# 1. Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'  # Update this with your MySQL root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating DB: {err}")

# 3. Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # Update this
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# 4. Create table user_data
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# 5. Insert data from CSV
def insert_data(connection, filename):
    try:
        cursor = connection.cursor()
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if user_id already exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print(f"Data from {filename} inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
