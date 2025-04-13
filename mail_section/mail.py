from dotenv import load_dotenv
import os
import json
import yagmail
import logging
import sqlite3

load_dotenv(dotenv_path="../config/.env")
SENDER_MAIL_ADDRESS = str(os.getenv("YOUR_EMAIL_USER"))
SENDER_MAIL_PASSWORD = str(os.getenv("YOUR_EMAIL_PASSWORD"))
RECEIVER_MAIL_ADDRESS = str(os.getenv("YOUR_RECEIVER_MAIL"))

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='mail_app.log',
    filemode='a'
)

class Mail:
    def load_template_json(template_file):
        try:
            with open(template_file, "r", encoding="utf-8") as file:
                template = json.load(file)
            logging.info("Template file loaded successfully.")
            return template
        except Exception as e:
            logging.error("An error occurred: "+str(e))
            raise

    def fetch_video_data(db_file_path, channel_id):
        try:
            conn = sqlite3.connect(db_file_path)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT name, title, published_at FROM videos
            JOIN channels ON videos.channel_id = channels.id
            WHERE videos.channel_id = (?)
            ORDER BY videos.published_at DESC
            """, (channel_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                logging.info("Video data was extracted from the database.")
                video_date = row[2][0:10]
                video_time = row[2][11:19]
                return {
                    "channel_name": row[0],
                    "video_name": row[1],
                    "publish_date": video_date,
                    "publish_time": video_time
                }
            else:
                logging.error("Video data not found in database.")
                return None
        except Exception as e:
            logging.error("Error while retrieving video data from database: " + str(e))
            return None

    def send_mail(template, sender_mail, sender_password, receiver_mail, context: dict):
        try:
            subject_template = template["subject"]
            body_template = template["body"]
            subject = subject_template.format(**context)
            body = body_template.format(**context)
        except Exception as e:
            logging.error("Mail content cannot created" + str(e))
            return

        try:
            yag = yagmail.SMTP(sender_mail, sender_password)
            yag.send(to=receiver_mail, subject=subject, contents=body)
            logging.info(f"Mail has sent to {receiver_mail} with {subject} subject")
        except Exception as e:
            logging.error("An error occured when sending mail: " + str(e))
