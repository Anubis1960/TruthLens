import subprocess

import PIL
import bs4
import requests
from cv2.typing import MatLike
from deep_translator import GoogleTranslator
import cv2
import numpy as np
import yt_dlp

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

def translate_text(text: str) -> str:
    return GoogleTranslator(source='auto', target='en').translate(text) # free to choose target

def fetch_image(url: str) -> np.ndarray | None:
    response = requests.get(url)
    # Convert the raw bytes into a NumPy array
    image_array = np.frombuffer(response.content, dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return None

    return image


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


def main():
    url = "https://miro.medium.com/v2/resize:fit:720/format:webp/0*xUYXAKdVxqYJsdZb.png"
    # soup = get_soup(url)
    # if soup is None:
    #     print(f"Failed to fetch {url}")
    #     return
    # print(extract_text(soup))
    # print(extract_links(soup, 'a'))
    # print(extract_images(soup, 'img'))
    # print(extract_video(soup, 'src'))
    # print(extract_title(soup))
    # print(extract_selector(soup, 'p'))
    total_frames = get_total_frames("video.mp4")
    print(f"Total frames: {total_frames}")
    #get 5 frames from the video between 0 and total_frames
    frames = np.random.randint(0, total_frames, 5)
    extract_frames("video.mp4", frames, "frame")


if __name__ == '__main__':
    main()