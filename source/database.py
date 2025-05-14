import sqlite3
import os
from dotenv import load_dotenv

# importing env file
load_dotenv(dotenv_path="../config/.env")

DATABASE_PATH = str("../data/video_downloader.db")
DATABASE_SCHEMA = str("../data/database_schema.sql")


class Database:
    def __init__(self, database_path, database_schema):
        self.database = database_path
        self.database_schema = str(database_schema)

    def creating_database(self):
        """Creating database.
        You must execute this function in first run"""
        # SCHEMA = str(os.getenv("DATABASE_SCHEMA"))
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        # Creating database tables
        with open(self.database_schema, "r") as sql_codes:
            sql_script = sql_codes.read()
            cursor.executescript(sql_script)

        conn.commit()
        conn.close()
        print("Database has created")

    def add_mail_address(self):
        """Adding mail channel to database"""
        mail_address = input("Insert your mail address: ")
        receiver_name = input("Insert receiver name: ")
        recevier_surname = input("Insert receiver surname: ")
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO mail_adresses (receiver_name,receiver_surname,receiver_mail)
                VALUES (?,?,?)
            """,(receiver_name,recevier_surname,mail_address))
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"There is an error: {e}")

        finally:
            conn.close()

    def delete_mail_address(self):
        """Delete a mail address from database"""
        mail_address = input("Enter the mail address: ")
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                        DELETE FROM mail_adresses
                        WHERE receiver_mail = ?
                    """, (mail_address,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"There is an error: {e}")

        finally:
            conn.close()

    def get_mail_addresses(self):
        """Get all mail addresses from database to list"""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receiver_mail FROM mail_adresses
        """)
        rows = cursor.fetchall()
        receivers = [row[0] for row in rows]
        return receivers

    def add_channel(self):
        """Adding your channels"""
        channel_id = input("Insert channel id: ")
        channel_name = input("Insert channel name: ")
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO channels (id, name)
                VALUES (?,?)
            """, (str(channel_id), str(channel_name)))
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"There is an error: {e}")

        finally:
            conn.close()

        print("The channel has added!")

    def delete_channel(self):
        channel_name = input("Enter channel name for delete: ")
        conn = sqlite3.connect(self.database)
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

    def get_channel_ids(self):
        """Getting channel id infos from database"""
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM channels")
            rows = cursor.fetchall()
            channel_ids = [row[0] for row in rows]
            conn.close()
            return channel_ids
        except Exception as e:
            print("There is an exception: " + str(e))

    def change_download_status(self, video_id):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE videos SET download = 1 WHERE id = (?)
        """, (video_id,))

        conn.commit()
        conn.close()


"""You must run this folder one time for creating database"""

#database = Database(DATABASE_PATH, DATABASE_SCHEMA)
#database.creating_database()
