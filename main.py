import asyncio
import requests

import snapinsta_downloader as snapinsta_downloader
import get_reel_details as get_reel_details
import utils as utils

from playwright.async_api import async_playwright

INSTA_AUDIO_IDENTIFIER='t2'
INSTA_VIDEO_IDENTIFIER='t16'

video_urls = set()

def handle_request(request):
    global video_urls

    url = request.url

    if '.mp4' not in url:
        return

    bytestart_index = url.find('&bytestart')
    clean_url = url[0:bytestart_index]

    video_urls.add(clean_url)


async def main():
    print('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'
    print(f'url: {insta_url}')

    # await snapinsta_downloader.download_insta_video(insta_url)
    # get_reel_details(instal_url)

    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        page = await browser.new_page()

        page.on('request', handle_request)
        await page.goto(insta_url)


    if len(video_urls) == 0:
        return

    count = 0
    for url in video_urls:
        response = requests.get(url, stream=True)

        video_type = 'audio' if INSTA_AUDIO_IDENTIFIER in url else 'video'

        name = f'{video_type}_{count}.mp4'
        count += 1

        with open(name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)



if __name__ == '__main__':
    asyncio.run(main())
