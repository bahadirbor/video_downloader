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
    def __init__(self, database_path):
        self.database = database_path

    def load_template_json(self, template_file):
        """Load template file in templates folder"""
        try:
            with open(template_file, "r", encoding="utf-8") as file:
                template = json.load(file)
            logging.info("Template file loaded successfully.")
            return template
        except Exception as e:
            logging.error("An error occurred: "+str(e))
            raise

    def fetch_video_data(self, channel_id):
        """Get video datas (name, video title, published time) from database"""
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT name, title, published_at FROM videos
            JOIN channels ON videos.channel_id = channels.id
            WHERE videos.channel_id = (?)
            ORDER BY videos.published_at DESC
            """, (channel_id,))
            row = cursor.fetchone() # Import video datas from database in a tuple
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

    def send_mail(self, template, sender_mail, sender_password, receiver_mails: list, context: dict):
        """Sending information mail to receiver mail address"""
        try:
            subject_template = template["subject"]
            body_template = template["body"]
            subject = subject_template.format(**context)
            body = body_template.format(**context)
        except Exception as e:
            logging.error("Mail content cannot created" + str(e))
            return

        for receiver_mail in receiver_mails:
            try:
                yag = yagmail.SMTP(sender_mail, sender_password)
                yag.send(to=receiver_mail, subject=subject, contents=body)
                logging.info(f"Mail has sent to {receiver_mail} with {subject} subject")
            except Exception as e:
                logging.error("An error occured when sending mail to "+receiver_mail+" : " + str(e))