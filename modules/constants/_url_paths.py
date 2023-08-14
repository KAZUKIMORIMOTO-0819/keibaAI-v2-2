import dataclasses


@dataclasses.dataclass(frozen=True)
class UrlPaths:
    DB_DOMAIN: str = 'https://db.netkeiba.com/'
    # レース結果テーブル、レース情報テーブル、払い戻しテーブルが含まれるページ
    RACE_URL: str = DB_DOMAIN + 'race/'
    # 馬の過去成績テーブルが含まれるページ
    HORSE_URL: str = DB_DOMAIN + 'horse/'
    # 血統テーブルが含まれるページ
    PED_URL: str = HORSE_URL + 'ped/'
    
    TOP_URL: str = 'https://race.netkeiba.com/top/'
    # 開催日程ページ
    CALENDAR_URL: str = TOP_URL + 'calendar.html'
    # レース一覧ページ
    RACE_LIST_URL: str = TOP_URL + 'race_list.html'
    
    # 出馬表ページ
    SHUTUBA_TABLE: str = 'https://race.netkeiba.com/race/shutuba.html'