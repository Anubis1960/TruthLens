import os
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

SAVE_PATH=r"../temp"

def download_audio(url: str):
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
		audio_stream.download(output_path=SAVE_PATH, filename=f'{os.urandom(8).hex}.mp4')
		print('Video downloaded successfully!')

	except Exception as e:
		print(f"Some Error: {e}")


	except Exception as e:
		print(f"Some Error: {e}")

def download_video(url: str):
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

download_video("https://www.youtube.com/shorts/7WM-auFKhzM")