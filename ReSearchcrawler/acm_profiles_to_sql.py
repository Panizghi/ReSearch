import psycopg2
from psycopg2.extras import RealDictCursor

def test_connection():
    """Connect to db and output version."""
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="db",
            port="5432"
        )
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
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="db",
            port="5432"
        )
        cursor = connection.cursor()

        # Open and read the SQL file
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

if __name__ == "__main__":
    execute_sql_file("acm-fellows/profile_erd.sql")
