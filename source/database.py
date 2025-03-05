import sqlite3
import os
from dotenv import load_dotenv

# importing env file
load_dotenv(dotenv_path="../config/.env")

DATABASE_PATH = os.getenv("YOUR_DATABASE_URL")

def creating_database():
    """Creating database.
    You must execute this function in first run"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Creating database tables
    with open("../data/database_schema.sql", "r") as sql_codes:
        sql_script = sql_codes.read()
        cursor.executescript(sql_script)

    conn.commit()
    conn.close()

    print("Database has created")

def add_channel(channel_name,channel_id):
    """Adding your channels"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO channels (id, name)
            VALUES (?,?)
        """,(channel_id,channel_name))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"There is an error: {e}")
    finally:
        conn.close()

    print("The channel has added!")
