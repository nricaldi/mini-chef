import time
import random

def random_sleep(min=0.0, max=5.0):
    random_num = random.uniform(min, max)
    time.sleep(random_num)
