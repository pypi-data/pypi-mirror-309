import sqlite3
import csv

def csv_to_sql(csv_file, db_file, delimiter=',', table_name='csv_data'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Open the CSV file and get the column names
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter)
        column_names = next(csvreader)

    # Create the table with the column names
    column_definitions = ', '.join([f'"{col_name}" TEXT' for col_name in column_names])
    c.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions})''')

    # Insert the data into the table
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            values = ', '.join(['?' for _ in column_names])
            c.execute(f'INSERT INTO "{table_name}" VALUES ({values})', row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()