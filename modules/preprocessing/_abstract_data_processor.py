import pandas as pd
from abc import ABCMeta, abstractmethod

class AbstractDataProcessor(metaclass=ABCMeta):
    def __init__(self, filepath: str):
        self.__raw_data = pd.read_pickle(filepath)
        self.__preprocessed_data = self._preprocess()

    @abstractmethod
    def _preprocess(self):
        pass
    
    @property
    def raw_data(self):
        return self.__raw_data.copy()

    @property
    def preprocessed_data(self):
        return self.__preprocessed_data.copy()

    #rawデータを一つのファイルにまとめる運用に変更したため、以下は不要
    """def _delete_duplicate(self, old, new):
        filtered_old = old[~old.index.isin(new.index)]
        return pd.concat([filtered_old, new])

    def _read_pickle(self, path_list):
        df = pd.read_pickle(path_list[0])
        for path in path_list[1:]:
            df = self._delete_duplicate(df, pd.read_pickle(path))
        return df"""
