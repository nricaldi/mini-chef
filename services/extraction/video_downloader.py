import io
import logging
import requests

import utils as utils

from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def _extract_reel_id(insta_url: str) -> str:
    parsed_url = urlparse(insta_url)
    path_parts = [part for part in parsed_url.path.split('/') if part]

    if 'reel' not in path_parts:
        raise ValueError(f'Instagram reel id not found in URL: {insta_url}')

    reel_index = path_parts.index('reel')
    if reel_index + 1 >= len(path_parts):
        raise ValueError(f'Instagram reel id not found in URL: {insta_url}')

    return path_parts[reel_index + 1]


def _is_valid_instagram_url(insta_url: str) -> bool:
    parsed_url = urlparse(insta_url)
    hostname = parsed_url.hostname or ''
    return hostname in {'instagram.com', 'www.instagram.com'}


def _write_media(media: io.BytesIO, file_path: Path):
    if file_path.exists():
        logger.info(f'File lready exists: {file_path}')
        return

    with open(file_path, 'wb') as f:
        f.write(media.getbuffer()) 


async def download_reel_media(insta_url: str) -> dict[str, Path]:
    file_paths = {'audio': Path(), 'video': Path()}

    if not _is_valid_instagram_url(insta_url):
        raise ValueError(f'Video source is not from Instagram: {insta_url}')

    reel_id = _extract_reel_id(insta_url)
    logger.info(f'Reel id: {reel_id}')

    request_count = 0
    captured_urls: set[str] = set()

    def handle_request(request) -> None:
        nonlocal request_count
        request_count += 1
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

    logger.info(f'Request count: {request_count}')

    if not captured_urls:
        raise RuntimeError('No mp4 media found for this reel.')

    logger.info(f'Media file count: {len(captured_urls)}')

    for url in captured_urls:
        logger.debug(f'Url: {url}')

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
        except requests.RequestException as error:
            raise RuntimeError(f'Failed downloading media URL: {url}') from error

        buffer = io.BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            buffer.write(chunk)

        media_type = utils.get_buffer_media_type(buffer)
        if media_type != 'audio' and media_type != 'video':
            logger.info(f'Invalid media type: {media_type}')
            pass

        file_path = Path(f'{reel_id}_{media_type}.mp4')

        try:
            _write_media(buffer, file_path)
        except OSError as error:
            raise RuntimeError(f'Failed writing media {media_type} file: {file_path}') from error

        file_paths[media_type] = file_path

    return file_paths
