import time
import random
import asyncio

from playwright.async_api import async_playwright

def random_sleep(min=0.0, max=5.0):
    random_num = random.uniform(min, max)
    time.sleep(random_num)

async def main():
    print('Hello from mini-chef!')

    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://snapinsta.to/en/instagram-reels-downloader')

        random_sleep()

        input = page.get_by_placeholder('Paste url Instagram')
        button = page.get_by_role('button', name='Download')

        await input.hover()
        random_sleep()

        await input.click()
        random_sleep()

        await input.press_sequentially('https://www.instagram.com/beatrizcontreras.31/reel/DVEeGePD0Mh/')
        await button.hover()
        random_sleep()

        await button.click()
        random_sleep()

        download_button = page.locator('a[title="Download Video"]')
        random_sleep()
        random_sleep()

        async with page.expect_download() as download_info:
            await download_button.click()

        download = await download_info.value
        print(download.suggested_filename)  # e.g. "video.mp4"

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
