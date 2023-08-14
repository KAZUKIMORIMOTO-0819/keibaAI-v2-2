from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def prepare_chrome_driver():
    """
    Chromeのバージョンアップは頻繁に発生し、Webdriverとのバージョン不一致が多発するため、
    ChromeDriverManagerを使用し、自動的にバージョンを一致させる。
    """
    # ヘッドレスモード（ブラウザが立ち上がらない）
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    # Selenium3の場合
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # Selenium4の場合
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # 画面サイズをなるべく小さくし、余計な画像などを読み込まないようにする
    driver.set_window_size(50, 50)
    return driver
