from dotenv import load_dotenv
import os
import sqlite3
import googleapiclient.discovery

load_dotenv(dotenv_path="config/.env")

YOUTUBE_API = os.getenv("YOUR_YOUTUBE_API_KEY")
DATABASE_PATH = os.getenv("YOUR_DATABASE_URL")

def check_api_key():
    """Test our API key work"""
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API)
        request = youtube.channels().list(part="id", id="insert_any_youtube_channel_id")
        response = request.execute()
        if "items" in response:
            print("API key çalışıyor")
        else:
            print("API key üzerinde bir sorun var")
    except Exception as e:
        print("Bazı hatalar var: ", e)

youtube = googleapiclient.discovery.build("youtube","v3",developerKey=YOUTUBE_API)

def get_channels():
    """Get channels from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    return channels

def get_latest_videos(channel_id):
    """Get last videos from our channel list"""
    request = youtube.search().list(
        part="id,snippet",
        channelId = channel_id,
        order = "date",
        maxResults = 3
    )
    response = request.execute()
    return response.get("items",[])

def save_to_database(videos, channel_id):
    """Save video information to database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for video in videos:
        video_id = video["id"].get("videoId", video["id"].get("playlistId",""))
        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]

        cursor.execute("""
            INSERT OR IGNORE INTO videos (id,channel_id,title,published_at)
            VALUES (?,?,?,?,0)
        """,(video_id,channel_id,title,published_at))

    conn.commit()
    conn.close()

