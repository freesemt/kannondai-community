import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

video_urls = [
    "https://www.youtube.com/watch?v=T8sFBz1NvSs&list=PPSV",
    "https://www.youtube.com/watch?v=qhkpp_hPb9Y&list=PPSV",
    "https://www.youtube.com/watch?v=TEFuiwaLubk&list=PPSV",
    "https://www.youtube.com/watch?v=t6-BTKRUM58&list=PPSV",
    "https://www.youtube.com/watch?v=XcqTl7rmiss&list=PPSV",
]

loop_count = 100

options = Options()
# options.add_argument(r"--user-data-dir=C:\Users\Owner\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"--user-data-dir=C:\chrome-profile-test")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

time.sleep(1)
print("driver title (login):", driver.title)

# ここでYouTubeに遷移して以降の処理を続ける
driver.get("https://www.youtube.com/")
print("driver title (youtube):", driver.title)

for i in range(loop_count):
    print(f"Loop {i + 1}/{loop_count}")
    for j, url in enumerate(video_urls):
        print([j], "Opening URL:", url)
        driver.get(url)
        # 動画プレイヤーの全画面ボタンをクリック
        try:
            # 動画要素が現れるまで待つ
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.ytp-fullscreen-button"))
            )
            fullscreen_btn = driver.find_element(By.CSS_SELECTOR, "button.ytp-fullscreen-button")
            fullscreen_btn.click()
        except Exception as e:
            print("全画面ボタンのクリックに失敗:", e)
        # 動画の再生終了を待つ
        driver.execute_script("""
            var done = false;
            var player = document.querySelector('video');
            if (player) {
                player.onended = function(){ window.done = true; };
            }
            window.done = false;
        """)
        while True:
            done = driver.execute_script("return window.done;")
            if done:
                break
            time.sleep(1)
driver.quit()