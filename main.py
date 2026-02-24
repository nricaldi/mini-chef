import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def random_sleep(min=0.0, max=5.0):
    random_num = random.uniform(min, max)
    time.sleep(random_num)

def main():
    print('Hello from mini-chef!')

    driver = webdriver.Chrome()
    actions = ActionChains(driver)

    snapinsta_url = 'https://snapinsta.to/en/instagram-reels-downloader'
    snapinsta_url = 'https://www.instagram.com/reel/DTwaCXHESPd/?igsh=eXVjaTZ3azJwMGd1'
    driver.get(snapinsta_url)

    input_element = driver.find_element(By.ID, 's_input')
    random_sleep()

    actions.move_to_element(input_element).perform()
    random_sleep()

    actions.click(input_element).perform()
    random_sleep()

    url_to_download = 'https://www.instagram.com/reel/DTwaCXHESPd/?igsh=eXVjaTZ3azJwMGd1'
    actions.send_keys(url_to_download).perform()
    random_sleep()

    btn_element = driver.find_element(By.CLASS_NAME, 'btn-default')
    random_sleep(0.0, 1)

    actions.move_to_element(btn_element).perform()
    random_sleep()

    actions.click(btn_element).perform()
    random_sleep()

    driver.quit()

if __name__ == '__main__':
    main()
