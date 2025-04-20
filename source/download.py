import sqlite3
import os
import logging
import yt_dlp

log_dir = "..\\log"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "download.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class Download:
    def __init__(self, database_path):
        self.database = database_path

    def get_video_id(self):
        """Getting video id's from database"""
        try:
            conn = sqlite3.connect(self.database)
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

    def download_video(self, video_id: str, folder_path: str):
        """Videos download in our folder"""
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'outtmpl': os.path.join(folder_path, '%(title)s-%(id)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'noplaylist': True,
            'ffmpeg_location': 'C:\\ffmpeg\\bin\\',
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logging.info("Download is starting: %s", video_id)
                ydl.download([video_url])
                logging.info("Download has completed: %s", video_id)
        except Exception as e:
            logging.error("An error occured when downloading the video (%s): %s", video_id, e)






