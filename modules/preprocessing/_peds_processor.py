from sklearn.preprocessing import LabelEncoder
from ._abstract_data_processor import AbstractDataProcessor


class PedsProcessor(AbstractDataProcessor):
    """
    初期処理
    """
    def __init__(self, filepath):
        super().__init__(filepath)
    
    """
    前処理
    """
    def _preprocess(self):
        df = self.raw_data

        # カテゴリ変数に型変換を行う
        for column in df.columns:
            df[column] = LabelEncoder().fit_transform(df[column].fillna('Na'))
        return df.astype('category')
 