from source import api_integration
from source.database import Database
from source import download
from mail_section.mail import Mail
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="config/.env")
DATABASE_PATH = str(os.getenv("YOUR_DATABASE_URL_MAIN"))
YOUTUBE_API = str(os.getenv("YOUR_YOUTUBE_API_KEY"))
SENDER_MAIL_ADDRESS = str(os.getenv("YOUR_EMAIL_USER"))
SENDER_MAIL_PASSWORD = str(os.getenv("YOUR_MAIL_PASSWORD"))
RECEIVER_MAIL_ADDRESS = str(os.getenv("YOUR_RECEIVER_MAIL"))
TEMPLATE_PATH = str(os.getenv("NEW_VIDEO_TEMPLATE_PATH"))
DOWNLOAD_DIR = str(os.getenv("VIDEO_DOWNLOAD_DIR"))
DATABASE_SCHEMA = str(os.getenv("DATABASE_SCHEMA"))

if __name__ == "__main__":
    print("Welcome\n")
    while True:
        print("Press 1 for database operations")
        print("Press 2 for starting program")
        print("Press 0 for exit")
        decision = input("Make your choice: ")

        match decision:
            case "1":
                """Database Operations"""
                database = Database(DATABASE_PATH, DATABASE_SCHEMA)
                print("1.Add Channel\n2.Delete Channel")
                a = input("Input decision number:")
                if a == "1":
                    database.add_channel()
                elif a == "2":
                    database.delete_channel()

            case "2":
                """Video scraping, sending information from mail, download the videos"""
                database = Database(DATABASE_PATH, DATABASE_SCHEMA)
                mail = Mail(database.database)
                channels = api_integration.get_channels(DATABASE_PATH)
                for channel_id in channels:
                    videos = api_integration.get_latest_videos(channel_id, YOUTUBE_API)
                    api_integration.save_to_database(videos, channel_id, DATABASE_PATH)
                    channel_name = api_integration.get_channel_name(channel_id, DATABASE_PATH)
                    print(f"{channel_name} video list has updated!")

                try:
                    template = mail.load_template_json(TEMPLATE_PATH)

                except:
                    exit("Şablon dosyası yüklenemedi, program sonlandırılıyor.")

                channel_id_nums = database.get_channel_ids()
                for channel_id in channel_id_nums:
                    video_data = mail.fetch_video_data(str(channel_id))
                    if not video_data:
                        exit("Veritabanında video verisi bulunamadı, program sonlandırılıyor.")
                    mail.send_mail(template, SENDER_MAIL_ADDRESS, SENDER_MAIL_PASSWORD, RECEIVER_MAIL_ADDRESS,
                                   video_data)

                video_ids = download.get_video_id(DATABASE_PATH)

                for video_id in video_ids:
                    download.download_video(video_id, DOWNLOAD_DIR)
                    database.change_download_status(video_id)

            case "0":
                break






