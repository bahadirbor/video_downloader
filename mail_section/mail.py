from dotenv import load_dotenv
import os
import json
import yagmail
import logging

load_dotenv(dotenv_path="../config/.env")
SENDER_MAIL_ADDRESS = str(os.getenv("YOUR_EMAIL_USER"))
SENDER_MAIL_PASSWORD = str(os.getenv("YOUR_EMAIL_PASSWORD"))
RECEIVER_MAIL_ADDRESS = str(os.getenv("YOUR_RECEIVER_MAIL"))


def load_template_json():
    pass


def fetch_video_data():
    pass


def send_mail():
    pass