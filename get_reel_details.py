import html
import requests

from bs4 import BeautifulSoup

def get_reel_details(insta_url: str):
    response = requests.get(insta_url)
    soup = BeautifulSoup(response.text, 'lxml')

    description = 'og:description'

    soup.find(description)

    tag = soup.find('meta', attrs={'property': 'og:description'})
    raw = tag['content'] if tag else ''
    caption = html.unescape(raw).strip()

    print(caption)
