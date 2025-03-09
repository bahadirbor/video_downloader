import sqlite3
import os
from dotenv import load_dotenv

# importing env file
load_dotenv(dotenv_path="../config/.env")

DATABASE_PATH = str(os.getenv("YOUR_DATABASE_URL"))


def creating_database(path):
    """Creating database.
    You must execute this function in first run"""
    SCHEMA = str(os.getenv("DATABASE_SCHEMA"))
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Creating database tables
    with open(SCHEMA, "r") as sql_codes:
        sql_script = sql_codes.read()
        cursor.executescript(sql_script)

    conn.commit()
    conn.close()

    print("Database has created")

def add_channel(path):
    """Adding your channels"""
    channel_id = input("Insert channel id: ")
    channel_name = input("Insert channel name: ")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO channels (id, name)
            VALUES (?,?)
        """,(str(channel_id),str(channel_name)))
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        print(f"There is an error: {e}")
        
    finally:
        conn.close()

    print("The channel has added!")


creating_database(DATABASE_PATH)