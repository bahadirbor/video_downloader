from dotenv import load_dotenv
import os
import sqlite3
import googleapiclient.discovery

load_dotenv(dotenv_path="../config/.env")

"""Switch type to str for avoid errors"""
YOUTUBE_API = str(os.getenv("YOUR_YOUTUBE_API_KEY"))
DATABASE_PATH = str(os.getenv("YOUR_DATABASE_URL"))

def check_api_key():
    """Test our API key work(optional)"""
    try:
        youtube_test = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API)
        """If you wanna test your api you should fill id parameter in list(id=)"""
        request = youtube_test.channels().list(part="id", id="insert_any_youtube_channel_id")
        response = request.execute()
        if "items" in response:
            print("API key works")
        else:
            print("There is an issue at API key")
    except Exception as e:
        print("There is an error: ", e)

class Api:
    def __init__(self, database_path, developer_api_key):
        self.database = database_path
        self.developer_api_key = developer_api_key

    def get_channels(self):
        """Get channels from database"""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM channels")
        channels = [row[0] for row in cursor.fetchall()]
        conn.close()
        return channels

    def get_channel_name(self, channel_id):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM channels WHERE id = ?", (channel_id,))
        name = [row[0] for row in cursor.fetchall()]
        conn.close()
        return name[0]

    def get_latest_videos(self, channel_id):
        """Get last videos from our channel list"""
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.developer_api_key)
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            order="date",
            maxResults=3,
        )
        response = request.execute()
        return response.get("items", [])

    def save_to_database(self, videos, channel_id):
        """Save video information to database"""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        for video in videos:
            video_id = video["id"].get("videoId", video["id"].get("playlistId", ""))
            title = video["snippet"]["title"]
            published_at = video["snippet"]["publishedAt"]

            cursor.execute("""
                INSERT OR IGNORE INTO videos (id,channel_id,title,published_at)
                VALUES (?,?,?,?)
            """, (video_id, channel_id, title, published_at))

        conn.commit()
        conn.close()

