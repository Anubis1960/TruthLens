import os
import subprocess
import assemblyai as aai
import PIL
import bs4
import requests
from cv2.typing import MatLike
from deep_translator import GoogleTranslator
import cv2
import numpy as np
import yt_dlp
from dotenv import load_dotenv
from ..util.img.img_detect import predict_image
from ..util.news.news_detect import predict_text

# load .env file
load_dotenv()

# transcript api key
aai.settings.api_key = os.getenv('AAI_API_KEY')

def extract_domain(url: str) -> str:
    return url.split('/')[2]

def get_soup(url: str) -> bs4.BeautifulSoup | None:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        return None
    return bs4.BeautifulSoup(response.text, 'html.parser')

def extract_text(soup: bs4.BeautifulSoup) -> str:
    return soup.get_text(strip=True)

def extract_links(soup: bs4.BeautifulSoup, selector: str) -> list[str]:
    return [link['href'] for link in soup.select(selector)]

def extract_images(soup: bs4.BeautifulSoup, selector: str) -> list[str]:
    return [image['src'] for image in soup.select(selector)]

def extract_video(soup: bs4.BeautifulSoup, selector: str) -> list[str]:
    return [video['src'] for video in soup.select(selector)]

def extract_title(soup: bs4.BeautifulSoup) -> str:
    return soup.title.string

def extract_selector(soup: bs4.BeautifulSoup, selector: str) -> list[str]:
    return [element.string for element in soup.select(selector)]

def translate_text(text: str, target: str) -> str:
    return GoogleTranslator(source='auto', target=target).translate(text) # free to choose target

def fetch_image(url: str) -> np.ndarray | None:
    response = requests.get(url)
    # Convert the raw bytes into a NumPy array
    image_array = np.frombuffer(response.content, dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return None

    return image

def fetch_video_from_streaming_service(url: str, output_path: str) -> str:
    """
    Downloads a video from a streaming service using yt-dlp.

    :param url: The URL of the video on the streaming platform.
    :param output_path: The local file path where the video will be saved.
    """


    ydl_opts = {
        'outtmpl': f'{output_path}.mp4',  # Output file path
        'format': 'best',  # Choose the best quality format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(info_dict)
        print(f"Video successfully saved to {output_path}")
        return info_dict['title']
    except Exception as e:
        print(f"Error downloading video: {e}")
        return ""

def get_total_frames(video_path: str) -> int:
    """
    Retrieves the total number of frames in a video file.

    :param video_path: Path to the video file.
    :return: Total number of frames in the video.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Release the video capture object
    cap.release()

    return total_frames

def extract_frames(video_path: str, frames: np.ndarray, output_path: str):
    """
    Extracts specific frames from a video file and saves them as images.

    :param output_path:
    :param video_path: Path to the video file.
    :param frames: List of frame indices to extract.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    # Extract the frames
    for frame_number in frames:
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        ret, frame = cap.read()

        if not ret:
            print(f"Error reading frame {frame_number}")
            continue

        # Save the frame as an image
        image_path = f"{output_path}_{frame_number}.jpg"
        cv2.imwrite(image_path, frame)


    # Release the video capture object
    cap.release()

def analyze_frames(video_path: str, frames: np.ndarray) -> list:
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    sum = 0
    for frame_number in frames:
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        ret, frame = cap.read()

        if not ret:
            print(f"Error reading frame {frame_number}")
            continue

        sum += predict_image(frame)


    # Release the video capture object
    cap.release()

    return sum/len(frames)

def transcript(url: str) -> str:
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(url)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
        return ""
    else:
        print(transcript.text)
        return transcript.text

def main():
    # url = "https://sputnikglobe.com/20250306/china-confident-in-trade-war-advantage-over-us--1121620685.html"
    # soup = get_soup(url)
    # if soup is None:
    #     print(f"Failed to fetch {url}")
    #     return
    # title = extract_title(soup)
    # text = extract_text(soup)
    # predict_text(title, text)

    image_link = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmediapool.bmwgroup.com%2Fcache%2FP9%2F201507%2FP90190494%2FP90190494-bmw-e90-07-2015-2250px.jpg&f=1&nofb=1&ipt=7ad781a672ad435beef39c26bee8b2b16103e055e1e8679ff6214434a79fdc4a&ipo=images"
    img = fetch_image(image_link)
    if img is None:
        print("Failed to fetch image.")
        return

    prediction = predict_image(img)
    print(prediction)

if __name__ == '__main__':
    main()