import bs4
import requests
from deep_translator import GoogleTranslator
from src.util.img import img_detect
import cv2

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
    img = fetch_image(url)
    cv2.imshow("image", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()