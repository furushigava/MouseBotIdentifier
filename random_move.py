import pyautogui
import random
import time
time.sleep(3)
def random_move(duration=10, interval=1):
    screen_width, screen_height = pyautogui.size()
    end_time = time.time() + duration

    while time.time() < end_time:
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        pyautogui.moveTo(x, y, duration=0.25)
        time.sleep(interval)

if __name__ == "__main__":
    random_move(duration=9999, interval=1)
