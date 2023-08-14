import pandas as pd

from ._abstract_data_processor import AbstractDataProcessor
from modules.constants import HorseInfoCols as Cols


class HorseInfoProcessor(AbstractDataProcessor):
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

        # 生年月日をdatetime型に設定
        df['birthday'] = pd.to_datetime(df[Cols.BIRTHDAY], format="%Y年%m月%d日")

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
            #Cols.BIRTHDAY, # 生年月日
            #Cols.TRAINER, # 調教師
            #Cols.OWNER, # 馬主
            #Cols.BREEDER, # 生産者
            #Cols.REC_INFO, # 募集情報
            #Cols.ORIGIN, # 産地
            #Cols.PRICE, # セリ取引価格
            #Cols.WINNING_PRIZE, # 獲得賞金
            #Cols.TOTAL_RESULTS, # 通算成績
            #Cols.VICTORY_RACE, # 人気
            #Cols.RELATIVE_HORSE, # 近親馬
            'birthday',
            #'trainer_id',
            'owner_id',
            'breeder_id'
            ]]

        return df
