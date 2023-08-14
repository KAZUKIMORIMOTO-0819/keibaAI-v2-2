import datetime
import re
from selenium.webdriver.common.by import By
from modules.constants import UrlPaths
from ._prepare_chrome_driver import prepare_chrome_driver

def scrape_race_id_race_time_list(kaisai_date: str, waiting_time=10):
    """
    開催日をyyyymmddの文字列形式で指定すると、レースidとレース時刻の一覧が返ってくる関数。
    ChromeDriverは要素を取得し終わらないうちに先に進んでしまうことがあるので、
    要素が見つかるまで(ロードされるまで)の待機時間をwaiting_timeで指定。
    """
    race_id_list = []
    race_time_list = []
    driver = prepare_chrome_driver()
    # 取得し終わらないうちに先に進んでしまうのを防ぐため、暗黙的な待機（デフォルト10秒）
    driver.implicitly_wait(waiting_time)
    print('getting race_id_list')
    try:
        query = [
            'kaisai_date=' + str(kaisai_date)
        ]
        url = UrlPaths.RACE_LIST_URL + '?' + '&'.join(query)
        print('scraping: {}'.format(url))
        driver.get(url)

        a_list = driver.find_element(By.CLASS_NAME, 'RaceList_Box').find_elements(By.TAG_NAME, 'a')
        span_list = driver.find_element(By.CLASS_NAME, 'RaceList_Box')

        for a in a_list:
            race_id = re.findall('(?<=shutuba.html\?race_id=)\d+|(?<=result.html\?race_id=)\d+',
                a.get_attribute('href'))
            if len(race_id) > 0:
                race_id_list.append(race_id[0])

        for item in span_list.text.split('\n'):
            if ':' in item:
                race_time_list.append(item.split(' ')[0])

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return race_id_list, race_time_list

def create_active_race_id_list(minus_time=-50):
    """
    馬体重の発表されたレースidとレース時刻の一覧が返ってくる関数。
    馬体重の発表時刻は、引数で指定されたminus_timeをレース時刻から引いた時刻で算出します。
    """
    # 現在時刻を取得
    now_date = datetime.datetime.now().date().strftime('%Y%m%d')
    hhmm = datetime.datetime.now().strftime("%H:%M")
    print(now_date, hhmm)

    # レースidとレース時刻の一覧を取得
    race_id_list, race_time_list = scrape_race_id_race_time_list(now_date)

    # 現在時刻マイナス馬体重時刻を取得
    t_delta30 = datetime.timedelta(hours = 9, minutes = minus_time)
    JST30 = datetime.timezone(t_delta30, 'JST')
    now30 = datetime.datetime.now(JST30)
    hhmm_minus_time = now30.strftime("%H:%M")

    target_race_id_list = []
    target_race_time_list = []
    from_time = '09:15'

    for (race_id, race_time) in zip(race_id_list, race_time_list):

        # レース時刻より馬体重発表時刻を算出
        dt1 = datetime.datetime(int(now_date[:4]), int(now_date[4:6]),
            int(now_date[6:8]), int(race_time[0:2]), int(race_time[3:5]))
        dt2 = dt1 + datetime.timedelta(minutes = minus_time)
        announce_weight_time = dt2.strftime("%H:%M")

        # 1Rの場合は、前回のレース時刻を馬体重発表時刻に設定
        if '01' == race_id_list[10:12]:
            from_time = announce_weight_time

        # 前回のレース時刻 ＜ 現在時刻 ＜ レース時刻
        if (from_time < hhmm < race_time):
            target_race_id_list.append(race_id)
            target_race_time_list.append(race_time)
        # 現在時刻マイナス馬体重時刻 ＜ 馬体重発表時刻 ＜＝ 現在時刻
        elif (hhmm_minus_time < announce_weight_time <= hhmm):
            target_race_id_list.append(race_id)
            target_race_time_list.append(race_time)
        # 前回のレース時刻を退避
        from_time = race_time

    return target_race_id_list, target_race_time_list
