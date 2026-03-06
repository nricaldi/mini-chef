import html
import logging
import requests

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _get_soup_property(soup: BeautifulSoup, property: str) -> str:
    tag = soup.find('meta', attrs={'property': property})

    content = tag.get('content') if tag else ''
    return html.unescape(str(content)).strip()


def get_reel_details(insta_url: str):
    reel_details = {
        'title': '',
        'description': '',
        'image': ''
    }

    response = requests.get(insta_url)
    soup = BeautifulSoup(response.text, 'lxml')

    title = 'og:title'
    image = 'og:image'
    description = 'og:description'

    reel_details['title'] = _get_soup_property(soup, title)
    reel_details['image'] = _get_soup_property(soup, image)
    reel_details['description'] = _get_soup_property(soup, description)

    return reel_details
