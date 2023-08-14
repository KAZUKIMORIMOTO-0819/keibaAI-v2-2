import pandas as pd
import re

from ._abstract_data_processor import AbstractDataProcessor
from modules.constants import Master
from modules.constants import HorseResultsCols as Cols


class HorseResultsProcessor(AbstractDataProcessor):
    def __init__(self, filepath):
        """
        初期処理
        """
        super().__init__(filepath)
    
    def _preprocess(self):
        """
        前処理
        """
        df = self.raw_data

        # 着順に数字以外の文字列が含まれているものは、欠損値（NaN）に置き換える
        # サイト上のテーブルに存在する列名は、HorseResultsColsクラスで定数化している。
        df[Cols.RANK] = pd.to_numeric(df[Cols.RANK], errors='coerce')
        # 着順が欠損値（NaN）となったものを取り除く
        df.dropna(subset=[Cols.RANK], inplace=True)
        df[Cols.RANK] = df[Cols.RANK].astype(int)

        # 日付をdatetime型に設定
        df['date'] = pd.to_datetime(df[Cols.DATE])
        
        # 賞金のNaNを0で埋める
        df[Cols.PRIZE].fillna(0, inplace=True)
        
        # 1着の着差を0にする（xが0より小さい場合は、0、xが0以上の場合、xを返す）
        df[Cols.RANK_DIFF] = df[Cols.RANK_DIFF].map(lambda x: 0 if x<0 else x)
        
        # レース展開データ
        # n=1: 最初のコーナー位置, n=4: 最終コーナー位置
        def corner(x, n):
            if type(x) != str:
                return x
            elif n==4:
                return int(re.findall(r'\d+', x)[-1])
            elif n==1:
                return int(re.findall(r'\d+', x)[0])

        df['first_corner'] = df[Cols.CORNER].map(lambda x: corner(x, 1))
        df['final_corner'] = df[Cols.CORNER].map(lambda x: corner(x, 4))
        
        df['final_to_rank'] = df['final_corner'] - df[Cols.RANK]
        df['first_to_rank'] = df['first_corner'] - df[Cols.RANK]
        df['first_to_final'] = df['first_corner'] - df['final_corner']
        
        # 開催場所（数字以外の文字列を抽出）中央開催・地方開催・海外開催以外をその他（'99'）とする
        df[Cols.PLACE] = df[Cols.PLACE].str.extract(r'(\D+)')[0].map(Master.PLACE_DICT).fillna('99')
        
        # race_type（数字以外の文字列を抽出）
        df['race_type'] = df[Cols.RACE_TYPE_COURSE_LEN].str.extract(r'(\D+)')[0].map(Master.RACE_TYPE_DICT)
        # 距離は10の位を切り捨てる（数字の文字列を抽出）
        df['course_len'] = df[Cols.RACE_TYPE_COURSE_LEN].str.extract(r'(\d+)').astype(float) // 100

        # タイムの値を秒単位に変換
        # 準備
        baseformat = '%M:%S.%f'
        basetime = pd.to_datetime("00:00.0", format=baseformat)
        to_datetime = lambda x: pd.to_datetime(df[Cols.TIME], format=x, errors='coerce')
        # 秒単位へのフォーマット変換処理
        datetime_s = to_datetime(baseformat)
        # 「x:xx.x」フォーマット以外、許容するフォーマットを定義
        formats_additional = ['%M.%S.%f', '%M:%S:%f']
        for format_ in formats_additional:
            # 秒単位へのフォーマット変換処理
            datetime_s = datetime_s.fillna(to_datetime(format_))
        # フォーマット例外は欠損値になる
        df['time_seconds'] = (datetime_s - basetime).dt.total_seconds()

        # インデックス名を与える
        df.index.name = 'horse_id'

        # カラム抽出
        df = self._select_columns(df)

        return df

    def _select_columns(self, raw):
        """
        カラム抽出
        """
        df = raw.copy()[[
            #Cols.DATE, # 日付
            Cols.PLACE, # 開催
            Cols.WEATHER, # 天気
            Cols.R, # R
            Cols.RACE_NAME, # レース名
            # 映像
            Cols.N_HORSES, # 頭数
            Cols.WAKUBAN, # 枠番
            Cols.UMABAN, # 馬番
            Cols.TANSHO_ODDS, # オッズ
            Cols.POPULARITY, # 人気
            Cols.RANK, # 着順
            Cols.JOCKEY, # 騎手
            Cols.KINRYO, # 斤量
            #Cols.RACE_TYPE_COURSE_LEN, # 距離
            Cols.GROUND_STATE, # 馬場
            # 馬場指数
            #Cols.TIME, # タイム
            Cols.RANK_DIFF, # 着差
            # ﾀｲﾑ指数
            Cols.CORNER, # 通過
            Cols.PACE, # ペース
            Cols.NOBORI, # 上り
            Cols.WEIGHT_AND_DIFF, # 馬体重
            # 厩舎ｺﾒﾝﾄ
            # 備考
            # 勝ち馬(2着馬)
            Cols.PRIZE, # 賞金
            'date',
            'first_corner',
            'final_corner',
            'final_to_rank',
            'first_to_rank',
            'first_to_final',
            'race_type',
            'course_len',
            'time_seconds'
            ]]

        return df
