import asyncio

import snapinsta_downloader as snapinsta_downloader

async def main():
    print('Hello from mini-chef!')

    insta_url = 'https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/'

    await snapinsta_downloader.download_insta_video(insta_url)

if __name__ == '__main__':
    asyncio.run(main())
