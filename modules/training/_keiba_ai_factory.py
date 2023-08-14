import datetime
import os
import dill
from ._keiba_ai import KeibaAI
from ._data_splitter import DataSplitter


class KeibaAIFactory:
    """
    KeibaAIのインスタンスを作成するためのクラス
    """
    @staticmethod
    def create(featured_data, test_size = 0.3, valid_size = 0.3) -> KeibaAI:
        datasets = DataSplitter(featured_data, test_size, valid_size)
        return KeibaAI(datasets)

    @staticmethod
    def save(keibaAI: KeibaAI, version_name: str) -> None:
        """
        日付やバージョン、パラメータ、データなどを保存。
        保存先はmodels/(yyyymmdd)/(version_name).pickle。
        """
        yyyymmdd = datetime.date.today().strftime('%Y%m%d')
        # ディレクトリ作成
        os.makedirs(os.path.join('models', yyyymmdd), exist_ok=True)
        filepath_pickle = os.path.join('models', yyyymmdd, '{}.pickle'.format(version_name))
        with open(filepath_pickle, mode='wb') as f:
            dill.dump(keibaAI, f)
    
    @staticmethod
    def load(filepath: str) -> KeibaAI:
        with open(filepath, mode='rb') as f:
            return dill.load(f)
