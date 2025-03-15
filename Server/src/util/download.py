import os
import yt_dlp
from pytubefix import YouTube

SAVE_PATH=r"../temp"

def download_yt_audio(url: str):
	try:
		# object creation using YouTube
		yt = YouTube(url)

	except:
		# to handle exception
		print("Connection Error")

	# Get all streams for audio without video (only audio)
	audio_stream = yt.streams.filter(file_extension='mp4', progressive=False, only_audio=True).first()

	try:
		# downloading the video (without audio)
		audio_stream.download(output_path=SAVE_PATH, filename=f'{os.urandom(8).hex()}.mp4')
		print('Video downloaded successfully!')

	except Exception as e:
		print(f"Some Error: {e}")


def download_yt_video(url: str):
	try:
		# object creation using YouTube
		yt = YouTube(url)

	except:
		# to handle exception
		print("Connection Error")

	# Get all streams for video without audio (only video)
	video_stream = yt.streams.filter(file_extension='mp4', progressive=False, only_video=True).first()

	try:
		# downloading the video (without audio)
		video_stream.download(output_path=SAVE_PATH, filename=f"{os.urandom(8).hex()}.mp4")
		print('Video downloaded successfully!')

	except Exception as e:
		print(f"Some Error: {e}")


def download_tiktok_audio(url: str):
	# tiktok audio download
	ydl_opts = {
		'outtmpl': f'{os.urandom(8).hex()}.mp4',
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])