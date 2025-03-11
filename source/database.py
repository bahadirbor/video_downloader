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


def delete_channel(database_path):
    channel_name = input("Enter channel name for delete: ")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM channels WHERE name = (?) 
        """, (channel_name,))
        conn.commit()

    except Exception as e:
        print("There is an error: " + str(e))

    finally:
        conn.close()


def get_channel_ids(database_path):
    """Getting channel id infos from database"""
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM channels")
        rows = cursor.fetchall()
        channel_ids = [row[0] for row in rows]
        conn.close()
        return channel_ids
    except Exception as e:
        print("There is an exception: " + str(e))


def change_download_status(video_id, database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE videos SET download = 1 WHERE id = (?)
    """,(video_id,))

    conn.commit()
    conn.close()
