import dataclasses


@dataclasses.dataclass(frozen=True)
class HorseInfoCols:
    """
    サイト上のテーブル列名を、定数として持っておく。
    """
    BIRTHDAY: str = '生年月日'
    TRAINER: str = '調教師'
    OWNER: str = '馬主'
    REC_INFO: str = '募集情報'
    BREEDER: str = '生産者'
    ORIGIN: str = '産地'
    PRICE: str = 'セリ取引価格'
    WINNING_PRIZE: str = '獲得賞金'
    TOTAL_RESULTS: str = '通算成績'
    VICTORY_RACE: str = '主な勝鞍'
    RELATIVE_HORSE: str = '近親馬'