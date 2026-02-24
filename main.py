import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def main():
    print('Hello from mini-chef!')

    driver = webdriver.Chrome()
    actions = ActionChains(driver)

    snapinsta_url = 'https://snapinsta.to/en/instagram-reels-downloader'
    driver.get(snapinsta_url)

    input_element = driver.find_element(By.ID, 's_input')

    time.sleep(random.uniform(1.0, 3.0))

    actions.click(input_element).perform()

    time.sleep(random.uniform(1.0, 2.0))

    url_to_download = 'https://www.instagram.com/reel/DTwaCXHESPd/?igsh=eXVjaTZ3azJwMGd1'
    actions.send_keys(url_to_download).perform()

    time.sleep(random.uniform(1.0, 4))

    driver.quit()


if __name__ == '__main__':
    main()
