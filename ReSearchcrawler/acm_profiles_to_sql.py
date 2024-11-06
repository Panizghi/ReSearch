from dataclasses import dataclass

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

# values defined in docker-compose.yml
dbconfig = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "db",
    "port": "5432"
}


def test_connection():
    """Connect to db and output version."""
    try:
        connection = psycopg2.connect(**dbconfig)
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print("PostgreSQL version:", result)
    except Exception as e:
        print("Error connecting to the database:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def execute_sql_file(filename):
    """Run SQL file given path."""
    try:
        connection = psycopg2.connect(**dbconfig)
        cursor = connection.cursor()

        # open and read the SQL file
        with open(filename, 'r') as file:
            sql_commands = file.read()
        
        cursor.execute(sql_commands)
        connection.commit()
        print("SQL file executed successfully.")
    except Exception as e:
        print("Error executing SQL file:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def insert_author_data(filename):
    """Insert author data into db."""
    try:
        # <csv col name>: <db col name>
        column_map = {
            "LastName": "last_name",
            "GivenName": "given_name",
            "Location": "location",
            "Affiliation": "affiliation",
            "Interests": "interests"
        }

        conn = psycopg2.connect(**dbconfig)
        cursor = conn.cursor()

        # load csv into pandas
        df = pd.read_csv(filename, header=0)

        # dynamic query
        columns = ', '.join(column_map.values())
        values_placeholders = ', '.join(['%s'] * len(column_map))
        insert_query = f"INSERT INTO authors ({columns}) VALUES ({values_placeholders})"

        # Insert each row in the DataFrame into the PostgreSQL table
        for row in df.itertuples(index=False):
            cursor.execute(insert_query, [getattr(row, k) for k in column_map.keys()])
        
        # Commit the transaction
        conn.commit()
        print("Data loaded successfully.")
    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    execute_sql_file("acm-fellows/profile_erd.sql")
    insert_author_data("ReSearchcrawler/award_winner_list.csv")
