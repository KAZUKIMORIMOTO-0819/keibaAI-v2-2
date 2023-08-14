import optuna.integration.lightgbm as lgb_o

from modules.constants import ResultsCols


class DataSplitter:
    def __init__(self, featured_data, test_size, valid_size) -> None:
        self.__featured_data = featured_data
        self.train_valid_test_split(test_size, valid_size)

    def train_valid_test_split(self, test_size, valid_size):
        """
        訓練データとテストデータに分ける。さらに訓練データをoptuna用の訓練データと検証データに分ける。
        """
        self.__train_data, self.__test_data = self.__split_by_date(self.__featured_data, test_size=test_size)
        self.__train_data_optuna, self.__valid_data_optuna = self.__split_by_date(
            self.__train_data, test_size=valid_size
        )
        self.__lgb_train_optuna = lgb_o.Dataset(
            self.__train_data_optuna.drop(['rank', 'date', ResultsCols.TANSHO_ODDS], axis=1).values,
            self.__train_data_optuna['rank']
        )
        self.__lgb_valid_optuna = lgb_o.Dataset(
            self.__valid_data_optuna.drop(['rank', 'date', ResultsCols.TANSHO_ODDS], axis=1).values,
            self.__valid_data_optuna['rank']
        )
        # 説明変数と目的変数に分ける。開催はエラーなるので一度drop。
        self.__X_train = self.__train_data.drop(['rank', 'date', ResultsCols.TANSHO_ODDS], axis=1)
        self.__y_train = self.__train_data['rank']
        self.__X_test = self.__test_data.drop(['rank', 'date', ResultsCols.TANSHO_ODDS], axis=1)
        self.__y_test = self.__test_data['rank']

    def __split_by_date(self, df, test_size):
        """
        時系列に沿って訓練データとテストデータに分ける関数。test_sizeは0~1。
        """
        sorted_id_list = df.sort_values("date").index.unique()
        train_id_list = sorted_id_list[: round(len(sorted_id_list) * (1 - test_size))]
        test_id_list = sorted_id_list[round(len(sorted_id_list) * (1 - test_size)) :]
        train = df.loc[train_id_list]
        test = df.loc[test_id_list]
        return train, test

    @property
    def featured_data(self):
        return self.__featured_data

    @property
    def train_data(self):
        return self.__train_data

    @property
    def test_data(self):
        return self.__test_data

    @property
    def train_data_optuna(self):
        return self.__train_data_optuna

    @property
    def valid_data_optuna(self):
        return self.__valid_data_optuna

    @property
    def lgb_train_optuna(self):
        return self.__lgb_train_optuna

    @property
    def lgb_valid_optuna(self):
        return self.__lgb_valid_optuna

    @property
    def X_train(self):
        return self.__X_train

    @property
    def y_train(self):
        return self.__y_train

    @property
    def X_test(self):
        return self.__X_test

    @property
    def y_test(self):
        return self.__y_test

    @property
    def tansho_odds_test(self):
        return self.__test_data[ResultsCols.TANSHO_ODDS]
