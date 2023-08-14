import os
import pandas as pd

from ._data_merger import DataMerger
from modules.constants import LocalPaths, HorseResultsCols, Master

class FeatureEngineering:
    """
    使うテーブルを全てマージした後の処理をするクラス。
    新しい特徴量を作りたいときは、メソッド単位で追加していく。
    各メソッドは依存関係を持たないよう注意。
    """
    def __init__(self, data_merger: DataMerger):
        self.__data = data_merger.merged_data.copy()
        
    @property
    def featured_data(self):
        return self.__data
    
    def add_interval(self):
        """
        前走からの経過日数
        """
        self.__data['interval'] = (self.__data['date'] - self.__data['latest']).dt.days
        self.__data.drop('latest', axis=1, inplace=True)
        return self

    def add_agedays(self):
        """
        レース出走日から日齢を算出
        """
        # 日齢を算出
        self.__data['age_days'] = (self.__data['date'] - self.__data['birthday']).dt.days
        self.__data.drop('birthday', axis=1, inplace=True)
        return self
    
    def dumminize_weather(self):
        """
        weatherカラムをダミー変数化する
        """
        self.__data['weather'] = pd.Categorical(self.__data['weather'], Master.WEATHER_LIST)
        self.__data = pd.get_dummies(self.__data, columns=['weather'])
        return self
    
    def dumminize_race_type(self):
        """
        race_typeカラムをダミー変数化する
        """
        self.__data['race_type'] = pd.Categorical(
            self.__data['race_type'], list(Master.RACE_TYPE_DICT.values())
            )
        self.__data = pd.get_dummies(self.__data, columns=['race_type'])
        return self
    
    def dumminize_ground_state(self):
        """
        ground_stateカラムをダミー変数化する
        """
        self.__data['ground_state'] = pd.Categorical(
            self.__data['ground_state'], Master.GROUND_STATE_LIST
            )
        self.__data = pd.get_dummies(self.__data, columns=['ground_state'])
        return self
    
    def dumminize_sex(self):
        """
        sexカラムをダミー変数化する
        """
        self.__data['性'] = pd.Categorical(self.__data['性'], Master.SEX_LIST)
        self.__data = pd.get_dummies(self.__data, columns=['性'])
        return self
    
    def __label_encode(self, target_col: str):
        """
        引数で指定されたID（horse_id/jockey_id/trainer_id/owner_id/breeder_id）を
        ラベルエンコーディングして、Categorical型に変換する。
        """
        csv_path = os.path.join(LocalPaths.MASTER_DIR, target_col + '.csv')
        # ファイルが存在しない場合、空のDataFrameを作成
        if not os.path.isfile(csv_path):
            target_master = pd.DataFrame(columns=[target_col, 'encoded_id'])
        else:
            target_master = pd.read_csv(csv_path, dtype=object)

        # 後のmaxでエラーになるので、整数に変換
        target_master['encoded_id'] = target_master['encoded_id'].astype(int)

        # masterに存在しない、新しい情報を抽出
        new_target = self.__data[[target_col]][
            ~self.__data[target_col].isin(target_master[target_col])
            ].drop_duplicates(subset=[target_col])
        # 新しい情報を登録
        if len(target_master) > 0:
            new_target['encoded_id'] = [
                i+max(target_master['encoded_id']) for i in range(1, len(new_target)+1)
                ]
            # 整数に変換
            new_target['encoded_id'] = new_target['encoded_id'].astype(int)
        else: # まだ1行も登録されていない場合の処理
            new_target['encoded_id'] = [i for i in range(len(new_target))]
        # 元のマスタと繋げる
        new_target_master = pd.concat([target_master, new_target]).set_index(target_col)['encoded_id']
        # マスタファイルを更新
        new_target_master.to_csv(csv_path)
        # ラベルエンコーディング実行
        self.__data[target_col] = pd.Categorical(self.__data[target_col].map(new_target_master))
        return self
    
    def encode_horse_id(self):
        """
        horse_idをラベルエンコーディングして、Categorical型に変換する。
        """
        self.__label_encode('horse_id')
        return self
    
    def encode_jockey_id(self):
        """
        jockey_idをラベルエンコーディングして、Categorical型に変換する。
        """
        self.__label_encode('jockey_id')
        return self
    
    def encode_trainer_id(self):
        """
        trainer_idをラベルエンコーディングして、Categorical型に変換する。
        """
        self.__label_encode('trainer_id')
        return self

    def encode_owner_id(self):
        """
        owner_idをラベルエンコーディングして、Categorical型に変換する。
        """
        self.__label_encode('owner_id')
        return self

    def encode_breeder_id(self):
        """
        breeder_idをラベルエンコーディングして、Categorical型に変換する。
        """
        self.__label_encode('breeder_id')
        return self

    def dumminize_kaisai(self):
        """
        開催カラムをダミー変数化する
        """
        self.__data[HorseResultsCols.PLACE] = pd.Categorical(
            self.__data[HorseResultsCols.PLACE], list(Master.PLACE_DICT.values())
            )
        self.__data = pd.get_dummies(self.__data, columns=[HorseResultsCols.PLACE])
        return self

    def dumminize_around(self):
        """
        aroundカラムをダミー変数化する
        """
        self.__data['around'] = pd.Categorical(self.__data['around'], Master.AROUND_LIST)
        self.__data = pd.get_dummies(self.__data, columns=['around'])
        return self

    def dumminize_race_class(self):
        """
        race_classカラムをダミー変数化する
        """
        self.__data['race_class'] = pd.Categorical(self.__data['race_class'], Master.RACE_CLASS_LIST)
        self.__data = pd.get_dummies(self.__data, columns=['race_class'])
        return self