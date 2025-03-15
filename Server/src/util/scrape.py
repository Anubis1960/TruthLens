import bs4
import requests
from deep_translator import GoogleTranslator


def extract_domain(url: str) -> str:
    return url.split('/')[2]

def get_soup(url: str) -> bs4.BeautifulSoup | None:
    response = requests.get(url)
    if response.status_code != 200:
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

def fetch_image(url: str) -> bytes:
    response = requests.get(url)
    return response.content

def translate_text(text: str) -> str:
    return GoogleTranslator(source='auto', target='en').translate(text) # free to choose target

def main():
    url = "https://www.youtube.com/shorts/wfcxBBK3sOc"
    soup = get_soup(url)
    if soup is None:
        print(f"Failed to fetch {url}")
        return
    print(extract_text(soup))
    print(extract_links(soup, 'a'))
    print(extract_images(soup, 'img'))
    print(extract_video(soup, 'src'))
    print(extract_title(soup))
    print(extract_selector(soup, 'p'))


if __name__ == '__main__':
    main()