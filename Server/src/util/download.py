import os
import yt_dlp
from pytubefix import YouTube

SAVE_PATH=r"../temp"

def fetch_video_from_streaming_service(url: str, output_path: str):
    """
    Downloads a video from a streaming service using yt-dlp.

    :param url: The URL of the video on the streaming platform.
    :param output_path: The local file path where the video will be saved.
    """


    ydl_opts = {
        'outtmpl': output_path,  # Output file path
        'format': 'best',  # Choose the best quality format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Video successfully saved to {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

# download youtube video
fetch_video_from_streaming_service("https://www.youtube.com/shorts/3fQ3nAjT4e8", "video.mp4")
# download tiktok video
fetch_video_from_streaming_service("https://www.tiktok.com/@space.5j2/video/7306554369460243755?q=black%20hole&t=1742051916098", "video_tiktok.mp4")