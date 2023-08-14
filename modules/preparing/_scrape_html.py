import datetime
import re
import pandas as pd
import time
import os
from tqdm.auto import tqdm
from urllib.request import urlopen

from modules.constants import UrlPaths, LocalPaths

def scrape_html_race(race_id_list: list, skip: bool = True):
    """
    netkeiba.comのraceページのhtmlをスクレイピングしてdata/html/raceに保存する関数。
    skip=Trueにすると、すでにhtmlが存在する場合はスキップされ、Falseにすると上書きされる。
    返り値：新しくスクレイピングしたhtmlのファイルパス
    """
    updated_html_path_list = []
    for race_id in tqdm(race_id_list):
        # 保存するファイル名
        filename = os.path.join(LocalPaths.HTML_RACE_DIR, race_id+'.bin')
        # skipがTrueで、かつbinファイルがすでに存在する場合は飛ばす
        if skip and os.path.isfile(filename):
            print('race_id {} skipped'.format(race_id))
        else:
            # race_idからurlを作る
            url = UrlPaths.RACE_URL + race_id
            # 相手サーバーに負担をかけないように1秒待機する
            time.sleep(1)
            # スクレイピング実行
            html = urlopen(url).read()
            # 保存するファイルパスを指定
            with open(filename, 'wb') as f:
                # 保存
                f.write(html)
            updated_html_path_list.append(filename)
    return updated_html_path_list

def scrape_html_horse(horse_id_list: list, skip: bool = True):
    """
    netkeiba.comのhorseページのhtmlをスクレイピングしてdata/html/horseに保存する関数。
    skip=Trueにすると、すでにhtmlが存在する場合はスキップされ、Falseにすると上書きされる。
    返り値：新しくスクレイピングしたhtmlのファイルパス
    """
    updated_html_path_list = []
    for horse_id in tqdm(horse_id_list):
        # 保存するファイル名
        filename = os.path.join(LocalPaths.HTML_HORSE_DIR, horse_id+'.bin')
        # skipがTrueで、かつbinファイルがすでに存在する場合は飛ばす
        if skip and os.path.isfile(filename):
            print('horse_id {} skipped'.format(horse_id))
        else:
            # horse_idからurlを作る
            url = UrlPaths.HORSE_URL + horse_id
            # 相手サーバーに負担をかけないように1秒待機する
            time.sleep(1)
            # スクレイピング実行
            html = urlopen(url).read()
            # 保存するファイルパスを指定
            with open(filename, 'wb') as f:
                # 保存
                f.write(html)
            updated_html_path_list.append(filename)
    return updated_html_path_list

def scrape_html_ped(horse_id_list: list, skip: bool = True):
    """
    netkeiba.comのhorse/pedページのhtmlをスクレイピングしてdata/html/pedに保存する関数。
    skip=Trueにすると、すでにhtmlが存在する場合はスキップされ、Falseにすると上書きされる。
    返り値：新しくスクレイピングしたhtmlのファイルパス
    """
    updated_html_path_list = []
    for horse_id in tqdm(horse_id_list):
        # 保存するファイル名
        filename = os.path.join(LocalPaths.HTML_PED_DIR, horse_id+'.bin')
        # skipがTrueで、かつbinファイルがすでに存在する場合は飛ばす
        if skip and os.path.isfile(filename):
            print('horse_id {} skipped'.format(horse_id))
        else:
            # horse_idからurlを作る
            url = UrlPaths.PED_URL + horse_id
            # 相手サーバーに負担をかけないように1秒待機する
            time.sleep(1)
            # スクレイピング実行
            html = urlopen(url).read()
            # 保存するファイルパスを指定
            with open(filename, 'wb') as f:
                # 保存
                f.write(html)
            updated_html_path_list.append(filename)
    return updated_html_path_list

def scrape_html_horse_with_master(horse_id_list: list, skip: bool = True):
    """
    netkeiba.comのhorseページのhtmlをスクレイピングしてdata/html/horseに保存する関数。
    skip=Trueにすると、すでにhtmlが存在する場合はスキップされ、Falseにすると上書きされる。
    返り値：新しくスクレイピングしたhtmlのファイルパス
    また、horse_idごとに、最後にスクレイピングした日付を記録し、data/master/horse_results_updated_at.csvに保存する。
    """
    ### スクレイピング実行 ###
    print('scraping')
    updated_html_path_list = scrape_html_horse(horse_id_list, skip)
    # パスから正規表現でhorse_id_listを取得
    horse_id_list = [
        re.findall('horse\W(\d+).bin', html_path)[0] for html_path in updated_html_path_list
        ]
    # DataFrameにしておく
    horse_id_df = pd.DataFrame({'horse_id': horse_id_list})
    
    ### 取得日マスタの更新 ###
    print('updating master')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 現在日時を取得
    # ファイルが存在しない場合は、作成する
    if not os.path.isfile(LocalPaths.MASTER_RAW_HORSE_RESULTS_PATH):
        pd.DataFrame(columns=['horse_id', 'updated_at']).to_csv(LocalPaths.MASTER_RAW_HORSE_RESULTS_PATH, index=None)
    # マスタを読み込み
    master = pd.read_csv(LocalPaths.MASTER_RAW_HORSE_RESULTS_PATH, dtype=object)
    # horse_id列に新しい馬を追加
    new_master = master.merge(horse_id_df, on='horse_id', how='outer')
    # マスタ更新
    new_master.loc[new_master['horse_id'].isin(horse_id_list), 'updated_at'] = now
    # 列が入れ替わってしまう場合があるので、修正しつつ保存
    new_master[['horse_id', 'updated_at']].to_csv(LocalPaths.MASTER_RAW_HORSE_RESULTS_PATH, index=None)
    return updated_html_path_list
#TODO: scrape_html_horse_with_updated_atのテスト