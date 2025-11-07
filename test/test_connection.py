# test_connection.py
import psycopg
from configparser import ConfigParser

# Function to read the config file
def load_config():
    # We use a config file to keep passwords out of our code. This is non-negotiable for professionals.
    config = ConfigParser()
    config.read('config.ini')
    return config['postgresql']

# The main connection logic
def main():
    # Load the connection parameters
    params = load_config()

    # This 'with' block is a context manager. It's like having a personal assistant who automatically closes the door when you leave.
    print("Attempting to connect to the database...")
    with psycopg.connect(**params) as conn:
        # If we get here, the connection was successful!
        print("✅ Connection successful!")

        # Now let's get a 'cursor'. Think of it as asking your bank teller for a form to fill out.
        with conn.cursor() as cur:
            # Let's ask the database a very simple question to prove we can talk to it.
            cur.execute("SELECT 'Hello, World!';")
            result = cur.fetchone() # Get the first row of the result
            print(f"Database says: {result[0]}")

    # The context manager automatically closed the connection for us here.
    print("Connection is now closed.")

if __name__ == '__main__':
    main()