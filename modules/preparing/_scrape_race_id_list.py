import pandas as pd
import datetime
import time
import re
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.common.by import By

from modules.constants import UrlPaths
from ._prepare_chrome_driver import prepare_chrome_driver

def scrape_kaisai_date(from_: str, to_: str):
    """
    yyyy-mmの形式でfrom_とto_を指定すると、間のレース開催日一覧が返ってくる関数。
    to_の月は含まないので注意。
    """
    print('getting race date from {} to {}'.format(from_, to_))
    # 間の年月一覧を作成
    date_range = pd.date_range(start=from_, end=to_, freq="M")
    # 開催日一覧を入れるリスト
    kaisai_date_list = []
    for year, month in tqdm(zip(date_range.year, date_range.month), total=len(date_range)):
        # 取得したdate_rangeから、スクレイピング対象urlを作成する。
        # urlは例えば、https://race.netkeiba.com/top/calendar.html?year=2022&month=7 のような構造になっている。
        query = [
            'year=' + str(year),
            'month=' + str(month),
        ]
        url = UrlPaths.CALENDAR_URL + '?' + '&'.join(query)
        html = urlopen(url).read()
        time.sleep(1)
        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find('table', class_='Calendar_Table').find_all('a')
        for a in a_list:
            kaisai_date_list.append(re.findall('(?<=kaisai_date=)\d+', a['href'])[0])
    return kaisai_date_list

def scrape_race_id_list(kaisai_date_list: list, waiting_time=10):
    """
    開催日をyyyymmddの文字列形式でリストで入れると、レースid一覧が返ってくる関数。
    ChromeDriverは要素を取得し終わらないうちに先に進んでしまうことがあるので、
    要素が見つかるまで(ロードされるまで)の待機時間をwaiting_timeで指定。
    """
    race_id_list = []
    driver = prepare_chrome_driver()
    # 取得し終わらないうちに先に進んでしまうのを防ぐため、暗黙的な待機（デフォルト10秒）
    driver.implicitly_wait(waiting_time)
    max_attempt = 2
    print('getting race_id_list')
    for kaisai_date in tqdm(kaisai_date_list):
        try:
            query = [
                'kaisai_date=' + str(kaisai_date)
            ]
            url = UrlPaths.RACE_LIST_URL + '?' + '&'.join(query)
            print('scraping: {}'.format(url))
            driver.get(url)

            for i in range(1, max_attempt):
                try:
                    a_list = driver.find_element(By.CLASS_NAME, 'RaceList_Box').find_elements(By.TAG_NAME, 'a')
                    break
                except Exception as e:
                    # 取得できない場合は、リトライを実施
                    print(f'error:{e} retry:{i}/{max_attempt} waiting more {waiting_time} seconds')

            for a in a_list:
                race_id = re.findall('(?<=shutuba.html\?race_id=)\d+|(?<=result.html\?race_id=)\d+',
                    a.get_attribute('href'))
                if len(race_id) > 0:
                    race_id_list.append(race_id[0])
        except Exception as e:
            print(e)
            break

    driver.close()
    driver.quit()
    return race_id_list