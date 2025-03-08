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


def get_channels(path):
    """Get channels from database"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    return channels

def get_channel_name(channel_id,path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM channels WHERE id = ?",(channel_id,))
    name = [row[0] for row in cursor.fetchall()]
    conn.close()
    return name[0]

def get_latest_videos(channel_id, api):
    """Get last videos from our channel list"""
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api)
    request = youtube.search().list(
        part="id,snippet",
        channelId = channel_id,
        order = "date",
        maxResults = 3,
    )
    response = request.execute()
    return response.get("items",[])

def save_to_database(videos, channel_id, path):
    """Save video information to database"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    for video in videos:
        video_id = video["id"].get("videoId", video["id"].get("playlistId",""))
        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]

        cursor.execute("""
            INSERT OR IGNORE INTO videos (id,channel_id,title,published_at)
            VALUES (?,?,?,?)
        """,(video_id,channel_id,title,published_at))

    conn.commit()
    conn.close()

