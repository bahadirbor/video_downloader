import sqlite3
import os
import logging
import youtube_dl

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("download.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def get_video_id(database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM videos")
        rows = cursor.fetchall()
        video_ids = [row[0] for row in rows]
        conn.close()
        logging.info("Veri tabanından %d adet video id çekildi", len(video_ids))
        return video_ids
    except Exception as e:
        logging.error("Veri tabanından veri id çekilirken hata: %s", e)
        return []


