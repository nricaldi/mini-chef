import logging
import requests

from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

INSTA_AUDIO_IDENTIFIER = 't2'


def extract_reel_id(insta_url: str) -> str:
    parsed_url = urlparse(insta_url)
    path_parts = [part for part in parsed_url.path.split('/') if part]

    if 'reel' not in path_parts:
        raise ValueError(f'Instagram reel id not found in URL: {insta_url}')

    reel_index = path_parts.index('reel')
    if reel_index + 1 >= len(path_parts):
        raise ValueError(f'Instagram reel id not found in URL: {insta_url}')

    return path_parts[reel_index + 1]


def _has_mp4_header(file_path: Path) -> bool:
    with file_path.open('rb') as media_file:
        header = media_file.read(12)

    if len(header) < 12:
        return False

    return header[4:8] == b'ftyp'


def _is_valid_instagram_url(insta_url: str) -> bool:
    parsed_url = urlparse(insta_url)
    hostname = parsed_url.hostname or ''
    return hostname in {'instagram.com', 'www.instagram.com'}


def _write_media(response, name):
    if Path(name).exists():
        logging.info(f'Already created. Path: {name}')
        return

    with name.open('wb') as media_file:
        for chunk in response.iter_content(chunk_size=8192):
            media_file.write(chunk)

async def download_reel_media(insta_url: str) -> dict[str, Path]:
    file_paths = {'audio': Path(), 'video': Path()}

    if not _is_valid_instagram_url(insta_url):
        raise ValueError(f'Video source is not from Instagram: {insta_url}')

    reel_id = extract_reel_id(insta_url)
    logger.info(f'Reel id: {reel_id}')

    captured_urls: set[str] = set()

    def handle_request(request) -> None:
        url = request.url
        logger.debug(f'Captured request URL: {url}')

        if '.mp4' not in url:
            return

        clean_url = url.split('&bytestart=', 1)[0]
        captured_urls.add(clean_url)

    try:
        logger.info('Requesting page...')
        async with async_playwright() as playwright:
            browser = await playwright.firefox.launch(headless=False)
            page = await browser.new_page()

            page.on('request', handle_request)
            await page.goto(insta_url)
            await page.wait_for_timeout(3000)
            await browser.close()
    except Exception as error:
        raise RuntimeError('Unable to reach reel page.') from error

    if not captured_urls:
        raise RuntimeError('No mp4 media found for this reel.')

    for url in captured_urls:
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
        except requests.RequestException as error:
            raise RuntimeError(f'Failed downloading media URL: {url}') from error

        video_type = 'audio' if INSTA_AUDIO_IDENTIFIER in url else 'video'
        name = Path(f'{reel_id}_{video_type}.mp4')

        try:
            _write_media(response, name)
        except OSError as error:
            raise RuntimeError(f'Failed writing media file: {name}') from error

        if name.stat().st_size == 0 or not _has_mp4_header(name):
            raise RuntimeError(f'Downloaded file is not a valid MP4: {name}')

        file_paths[video_type] = name

    return file_paths
