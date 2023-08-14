from abc import ABCMeta, abstractstaticmethod
import pandas as pd

from modules.constants import ResultsCols

class AbstractBetPolicy(metaclass=ABCMeta):
    """
    クラスの型を決めるための抽象クラス。
    """
    @abstractstaticmethod
    def judge(score_table, **params):
        """
        bet_dictは{race_id: {馬券の種類: 馬番のリスト}}の形式で返す。

        例)
        {'202101010101': {'tansho': [6, 8], 'fukusho': [4, 5]},
        '202101010102': {'tansho': [1], 'fukusho': [4]},
        '202101010103': {'tansho': [6], 'fukusho': []},
        '202101010104': {'tansho': [5], 'fukusho': [11]},
        ...}
        """
        pass

class BetPolicyTansho:
    """
    thresholdを超えた馬に単勝で賭ける戦略。
    """
    @staticmethod
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'tansho'}).T.to_dict()
        return bet_dict

class BetPolicyFukusho:
    """
    thresholdを超えた馬に複勝で賭ける戦略。
    """
    @staticmethod
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'fukusho'}).T.to_dict()
        return bet_dict

class BetPolicyUmarenBox:
    """
    thresholdを超えた馬に馬連BOXで賭ける戦略。
    """
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_df = bet_df[bet_df[ResultsCols.UMABAN].apply(len) >= 2]
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'umaren'}).T.to_dict()
        return bet_dict

class BetPolicyUmatanBox:
    """
    thresholdを超えた馬に馬単BOXで賭ける戦略。
    """
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_df = bet_df[bet_df[ResultsCols.UMABAN].apply(len) >= 2]
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'umatan'}).T.to_dict()
        return bet_dict

class BetPolicyWideBox:
    """
    thresholdを超えた馬にワイドBOXで賭ける戦略。
    """
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_df = bet_df[bet_df[ResultsCols.UMABAN].apply(len) >= 2]
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'wide'}).T.to_dict()
        return bet_dict

class BetPolicySanrenpukuBox:
    """
    thresholdを超えた馬に三連複BOXで賭ける戦略。
    """
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_df = bet_df[bet_df[ResultsCols.UMABAN].apply(len) >= 3]
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'sanrenpuku'}).T.to_dict()
        return bet_dict

class BetPolicySanrentanBox:
    """
    thresholdを超えた馬に三連単BOXで賭ける戦略。
    """
    def judge(score_table: pd.DataFrame, threshold: float) -> dict:
        filtered_table = score_table[score_table['score'] >= threshold]
        bet_df = filtered_table.groupby(level=0)[ResultsCols.UMABAN].apply(list).to_frame()
        bet_df = bet_df[bet_df[ResultsCols.UMABAN].apply(len) >= 3]
        bet_dict = bet_df.rename(columns={ResultsCols.UMABAN: 'sanrentan'}).T.to_dict()
        return bet_dict

class BetPolicyUmatanNagashi:
    """
    threshold1を超えた馬を軸にし、threshold2を超えた馬を相手にして馬単で賭ける。（未実装）
    """
    def judge(score_table: pd.DataFrame, threshold1: float, threshold2: float) -> dict:
        bet_dict = {}
        filtered_table = score_table.query('score >= @threshold2')
        filtered_table['flg'] = filtered_table['score'].map(lambda x: 'jiku' if x >= threshold1 else 'aite')
        for race_id, table in filtered_table.groupby(level=0):
            bet_dict_1R = {}
            bet_dict_1R['tansho'] = list(table.query('flg == "tansho"')[ResultsCols.UMABAN])
            bet_dict_1R['fukusho'] = list(table.query('flg == "fukusho"')[ResultsCols.UMABAN])
            bet_dict[race_id] = bet_dict_1R
        return bet_dict
