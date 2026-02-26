import asyncio
import requests
import html

import snapinsta_downloader as snapinsta_downloader

from bs4 import BeautifulSoup

async def main():
    print('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'
    print(f'url: {insta_url}')

    # await snapinsta_downloader.download_insta_video(insta_url)

    response = requests.get(insta_url)
    soup = BeautifulSoup(response.text, 'lxml')

    description = 'og:description'

    soup.find(description)

    tag = soup.find('meta', attrs={'property': 'og:description'})
    raw = tag['content'] if tag else ''
    caption = html.unescape(raw).strip()

    print(caption)



if __name__ == '__main__':
    asyncio.run(main())
