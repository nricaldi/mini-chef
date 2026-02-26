from playwright.async_api import async_playwright

import utils as utils

async def download_insta_video(insta_url: str):
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://snapinsta.to/en/instagram-reels-downloader')

        utils.random_sleep()

        input = page.get_by_placeholder('Paste url Instagram')
        button = page.get_by_role('button', name='Download')

        await input.hover()
        utils.random_sleep()

        await input.click()
        utils.random_sleep()

        await input.press_sequentially(insta_url)
        await button.hover()
        utils.random_sleep()

        await button.click()
        utils.random_sleep()

        download_button = page.locator('a[title="Download Video"]')
        utils.random_sleep()
        utils.random_sleep()

        async with page.expect_download() as download_info:
            await download_button.click()

        download = await download_info.value
        print(download.suggested_filename)  # e.g. "video.mp4"

        await browser.close()
