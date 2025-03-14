import bs4
import requests

def extract_domain(url: str) -> str:
    return url.split('/')[2]

def get_soup(url: str) -> bs4.BeautifulSoup:
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, 'html.parser')

def extract_text(soup: bs4.BeautifulSoup) -> str:
    return soup.get_text(separator=' ', strip=True)

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

if __name__ == '__main__':
    url = 'https://www.bbc.co.uk/news/articles/cg70y3ydmdno'
    soup = get_soup(url)
    print(extract_text(soup))
    print(extract_links(soup, 'a'))
    print(extract_images(soup, 'img'))
    print(extract_video(soup, 'video'))
    print(extract_title(soup))
    print(extract_selector(soup, 'p'))