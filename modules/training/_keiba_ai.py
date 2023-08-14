import pandas as pd
from modules.policies import AbstractBetPolicy
from ._model_wrapper import ModelWrapper
from ._data_splitter import DataSplitter
from modules.policies import AbstractScorePolicy

class KeibaAI:
    """
    モデルの訓練や読み込み、実際に賭けるなどの処理を実行するクラス。
    """
    def __init__(self, datasets: DataSplitter):
        self.__datasets = datasets
        self.__model_wrapper = ModelWrapper()

    @property
    def datasets(self):
        return self.__datasets

    def train_with_tuning(self):
        """
        optunaでのチューニング後、訓練させる。
        """
        self.__model_wrapper.tune_hyper_params(self.__datasets)
        self.__model_wrapper.train(self.__datasets)

    def train_without_tuning(self):
        """
        ハイパーパラメータチューニングをスキップして訓練させる。
        """
        self.__model_wrapper.train(self.__datasets)

    def get_params(self):
        """
        ハイパーパラメータを取得
        """
        return self.__model_wrapper.params

    def set_params(self, params):
        """
        ハイパーパラメータを外部から設定。
        """
        self.__model_wrapper.set_params(params)

    def feature_importance(self, num_features=20):
        return self.__model_wrapper.feature_importance[:num_features]

    def calc_score(self, X: pd.DataFrame, score_policy: AbstractScorePolicy):
        """
        score_policyを元に、馬の「勝ちやすさスコア」を計算する。
        """
        return score_policy.calc(self.__model_wrapper.lgb_model, X)

    def decide_action(self, score_table: pd.DataFrame,
        bet_policy: AbstractBetPolicy, **params) -> dict:
        """
        bet_policyを元に、賭ける馬券を決定する。paramsにthresholdを入れる。
        """
        actions = bet_policy.judge(score_table, **params)

        return actions
