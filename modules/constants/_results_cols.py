import dataclasses

@dataclasses.dataclass(frozen=True)
class ResultsCols:
    """
    サイト上のテーブル列名を、定数として持っておく。
    """
    RANK: str = '着順'
    WAKUBAN: str = '枠番'
    UMABAN: str = '馬番'
    HORSE_NAME: str = '馬名'
    SEX_AGE: str = '性齢'
    KINRYO: str = '斤量'
    JOCKEY: str = '騎手'
    TIME: str = 'タイム'
    RANK_DIFF: str = '着差'
    # 通過
    # 上がり
    TANSHO_ODDS: str = '単勝'
    POPULARITY: str = '人気'
    WEIGHT_AND_DIFF: str = '馬体重'
    TRAINER: str = '調教師'