import pandas as pd

from ._data_merger import DataMerger
from modules.preprocessing import ShutubaTableProcessor
from modules.preprocessing import HorseResultsProcessor
from modules.preprocessing import HorseInfoProcessor
from modules.preprocessing import PedsProcessor

class ShutubaDataMerger(DataMerger):
    def __init__(self,
                 shutuba_table_processor: ShutubaTableProcessor, 
                 horse_results_processor: HorseResultsProcessor,
                 horse_info_processor: HorseInfoProcessor,
                 peds_processor: PedsProcessor, 
                 target_cols: list, 
                 group_cols: list
                 ):
        """
        初期処理
        """
        # レース結果テーブル（前処理後）
        self._results = shutuba_table_processor.preprocessed_data
        # 馬の過去成績テーブル（前処理後）
        self._horse_results = horse_results_processor.preprocessed_data
        # 馬の基本情報テーブル（前処理後）
        self._horse_info = horse_info_processor.preprocessed_data
        # 血統テーブル（前処理後）
        self._peds = peds_processor.preprocessed_data
        # 集計対象列
        self._target_cols = target_cols
        # horse_idと一緒にターゲットエンコーディングしたいカテゴリ変数
        self._group_cols = group_cols
        # 全てのマージが完了したデータ
        self._merged_data = pd.DataFrame()
        # 日付(date列)ごとに分かれたレース結果
        self._separated_results_dict = {}
        # レース結果データのdateごとに分かれた馬の過去成績
        self._separated_horse_results_dict = {}
        
    def merge(self):
        """
        マージ処理
        """
        self._merge_horse_results()
        self._merge_horse_info()
        self._merge_peds()