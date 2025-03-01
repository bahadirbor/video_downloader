import sqlite3
import os
from dotenv import load_dotenv

# importing env file
load_dotenv(dotenv_path="../config/.env")

DATABASE_PATH = os.getenv("YOUR_DATABASE_URL")

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

with open("../data/database_schema.sql", "r") as sql_codes:
    sql_script = sql_codes.read()
    cursor.executescript(sql_script)

conn.commit()
conn.close()

print(f"Database has created: {DATABASE_PATH}")