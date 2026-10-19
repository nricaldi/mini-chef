import html
import logging
from pydantic import HttpUrl
import requests

from bs4 import BeautifulSoup

from app.extraction.models import VideoMetadata


logger = logging.getLogger(__name__)


def _get_soup_property(soup: BeautifulSoup, property: str) -> str:
    tag = soup.find('meta', attrs={'property': property})

    content = tag.get('content') if tag else ''
    return html.unescape(str(content)).strip()


def fetch_metadata(url: HttpUrl):
    response = requests.get(str(url))
    soup = BeautifulSoup(response.text, 'lxml')

    return VideoMetadata(
        description=_get_soup_property(soup, 'og:description'),
        image_url=_get_soup_property(soup, 'og:image'),
        title=_get_soup_property(soup, 'og:title'),
    )
