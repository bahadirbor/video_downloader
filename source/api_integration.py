from dotenv import load_dotenv
import os
import sqlite3
import googleapiclient.discovery

load_dotenv(dotenv_path="config/.env")

YOUTUBE_API = os.getenv("YOUR_YOUTUBE_API_KEY")

# Youtube API anahtarının çalışma durumunu kontrol ettik
def check_api_key():
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API)
        request = youtube.channels().list(part="id", id="UCsGwZ3006CuJWcA5J3UPVWw")
        response = request.execute()
        if "items" in response:
            print("API key çalışıyor")
        else:
            print("API key üzerinde bir sorun var")
    except Exception as e:
        print("Bazı hatalar var: ", e)


