import os
from dotenv import load_dotenv
from source.api_integration import Api
from source.database import Database
from source.download import Download
from mail_section.mail import Mail

load_dotenv(dotenv_path="config/.env")

"""Convert env info types to str to avoid errors"""
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
        print("Press 3 for download video with video url")
        print("Press 0 for exit")
        decision = input("Make your choice: ")

        match decision:
            case "1":
                """Database Operations"""
                database = Database(DATABASE_PATH, DATABASE_SCHEMA)
                print("1.Add Channel\n2.Delete Channel\n3.Add Receiver\n4.Delete Receiver")
                a = input("Input decision number:")
                match a:
                    case "1":
                        database.add_channel()
                    case "2":
                        database.delete_channel()
                    case "3":
                        database.add_mail_address()
                    case "4":
                        database.delete_mail_address()

            case "2":
                """Video scraping, sending information from mail, download the videos"""
                database = Database(DATABASE_PATH, DATABASE_SCHEMA)
                mail = Mail(database.database)
                api = Api(database.database, YOUTUBE_API)
                channels = api.get_channels()
                download = Download(database.database)
                for channel_id in channels:
                    videos = api.get_latest_videos(channel_id)
                    api.save_to_database(videos, channel_id)
                    channel_name = api.get_channel_name(channel_id)
                    print(f"{channel_name} video list has updated!")

                try:
                    template = mail.load_template_json(TEMPLATE_PATH)

                except:
                    exit("Şablon dosyası yüklenemedi, program sonlandırılıyor.")

                channel_id_nums = database.get_channel_ids()
                receiver_mails = database.get_mail_addresses()
                print(receiver_mails)
                for channel_id in channel_id_nums:
                    video_data = mail.fetch_video_data(str(channel_id))
                    if not video_data:
                        exit("Veritabanında video verisi bulunamadı, program sonlandırılıyor.")
                    mail.send_mail(template, SENDER_MAIL_ADDRESS, SENDER_MAIL_PASSWORD, receiver_mails, video_data)

                video_ids = download.get_video_id()

                for video_id in video_ids:
                    download.download_video(video_id, DOWNLOAD_DIR)
                    database.change_download_status(video_id)

            case "3":
                download = Download(DATABASE_PATH)
                video_url = input("Enter your video url: ")
                video_url = video_url.split("=")[1]
                download.download_video(video_url, DOWNLOAD_DIR)

            case "0":
                break