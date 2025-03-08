from source import api_integration
import source.database
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="config/.env")
DATABASE_PATH = str(os.getenv("YOUR_DATABASE_URL_MAIN"))
YOUTUBE_API = str(os.getenv("YOUR_YOUTUBE_API_KEY"))

if __name__ == "__main__":
    print("Welcome\n")
    while True:
        print("Press 1 for add new channel from database")
        print("Press 2 for start the program")
        print("Press 0 for exit")
        decision = input("Make your choice: ")

        if decision == "1":
            """Add new youtube channel"""
            source.database.add_channel(DATABASE_PATH)
        elif decision == "2":
            """Scraping new videos and insert to database"""
            channels = api_integration.get_channels(DATABASE_PATH)
            for channel_id in channels:
                videos = api_integration.get_latest_videos(channel_id, YOUTUBE_API)
                api_integration.save_to_database(videos,channel_id, DATABASE_PATH)
                channel_name = api_integration.get_channel_name(channel_id, DATABASE_PATH)
                print(f"{channel_name} video list has updated!")
        elif decision == "0":
            break

