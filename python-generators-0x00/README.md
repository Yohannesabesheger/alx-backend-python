📁 python-generators-0x00 – Getting Started with Python Generators
🔍 Project Objective
The goal of this project is to learn how to work with Python generators by applying them in a real-world context: streaming data from a MySQL database one row at a time.

This project includes:

Setting up a MySQL database (ALX_prodev)

Creating a table (user_data)

Inserting data from a CSV file (user_data.csv)

Preparing to stream rows from the database using Python generators

📌 Task 0: Setup and Seed the Database
✅ Requirements:
Create the database ALX_prodev (if it doesn't exist)

Create the table user_data with the following schema:

user_id: UUID, Primary Key, Indexed

name: VARCHAR, NOT NULL

email: VARCHAR, NOT NULL

age: DECIMAL, NOT NULL

Load data from user_data.csv into the table

🛠️ File Descriptions
seed.py: Contains functions to connect to MySQL, create the database and table, and insert data from CSV.

connect_db() – Connect to MySQL server

create_database(connection) – Create ALX_prodev if not exists

connect_to_prodev() – Connect to the ALX_prodev database

create_table(connection) – Create the user_data table

insert_data(connection, filename) – Insert data from user_data.csv

0-main.py: Runs the above steps and verifies the database creation and data insertion.

user_data.csv: Sample data file to populate the table.

▶️ How to Run
Ensure MySQL server is running and accessible.

Update seed.py with your correct MySQL credentials.

Run the main script:

bash
Copy
Edit
chmod +x 0-main.py
./0-main.py
📘 Coming Next
In the next task, you will implement a Python generator that streams rows from the user_data table one by one, allowing for efficient memory usage when processing large datasets.
