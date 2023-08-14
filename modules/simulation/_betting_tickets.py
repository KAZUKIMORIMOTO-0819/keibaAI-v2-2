from modules.preprocessing import ReturnProcessor
from itertools import permutations
from scipy.special import comb

class BettingTickets:
    """
    馬券の買い方と、賭けた時のリターンを計算する。
    """
    def __init__(self, returnProcessor: ReturnProcessor) -> None:
        self.__returnTables = returnProcessor.preprocessed_data
        self.__returnTablesTansho = self.__returnTables['tansho']
        self.__returnTablesFukusho = self.__returnTables['fukusho']
        self.__returnTablesUmaren = self.__returnTables['umaren']
        self.__returnTablesUmatan = self.__returnTables['umatan']
        self.__returnTablesWide = self.__returnTables['wide']
        self.__returnTablesSanrenpuku = self.__returnTables['sanrenpuku']
        self.__returnTablesSanrentan = self.__returnTables['sanrentan']

    def bet_tansho(self, race_id: str, umaban: list, amount: float):
        """
        race_id: レースid。
        umaban: 賭けたい馬番をリストで入れる。一頭のみ賭けたい場合もリストで入れる。
        amount: 1枚に賭ける額。
        """
        # 賭ける枚数
        n_bets = len(umaban)
        if n_bets == 0:
            return 0, 0, 0
        else:
            # 賭けた合計額
            bet_amount = n_bets * amount
            # 賭けるレースidに絞った単勝の払い戻し表
            table_1R = self.__returnTablesTansho.loc[race_id]
            # 的中判定
            hit = table_1R['win'] in umaban
            # 払い戻し合計額
            return_amount = hit * table_1R['return'] * amount / 100
            return n_bets, bet_amount, return_amount

    def bet_fukusho(self, race_id: str, umaban: list, amount: float):
        """
        引数の考え方は単勝と同様。
        """
        # 賭ける枚数
        n_bets = len(umaban)
        if n_bets == 0:
            return 0, 0, 0
        else:
            # 賭けた合計額
            bet_amount = n_bets * amount
            # 賭けるレースidに絞った複勝の払い戻し表
            table_1R = self.__returnTablesFukusho.loc[race_id]
            # 1~3着それぞれに的中判定
            hits = table_1R[['win_0', 'win_1', 'win_2']].isin(umaban)
            # 払い戻し合計額
            return_amount = sum(
                hits.values * table_1R[['return_0', 'return_1', 'return_2']].values \
                    * amount / 100
            )
            return n_bets, bet_amount, return_amount

    def bet_umaren_box(self, race_id: str, umaban: list, amount: float):
        """
        馬連BOX馬券。1枚のみ買いたい場合もこの関数を使う。
        """
        # 賭ける枚数
        # 例）4C2（4コンビネーション2）
        n_bets = comb(len(umaban), 2)
        if n_bets == 1:
            #print('例外')
            return 0, 0, 0
        else:
            # 賭けた合計額
            bet_amount = n_bets * amount
            # 賭けるレースidに絞った馬連払い戻し表
            table_1R = self.__returnTablesUmaren.loc[race_id]
            # 的中判定
            hit = set(table_1R[['win_0', 'win_1']]).issubset(set(umaban))
            # 払い戻し合計額
            return_amount = hit * table_1R['return'] * amount / 100
        return n_bets, bet_amount, return_amount

    def _bet_umatan(self, race_id: str, umaban: list, amount: float):
        """
        馬単を一枚のみ賭ける場合の関数。umabanは[1着予想, 2着予想]の形で馬番を入れる。
        """
        #len(umaban) != 2の時の例外処理
        if len(umaban) != 2:
            print('例外')
            return 0, 0, 0

        # 賭けるレースidに絞った馬単払い戻し表
        table_1R = self.__returnTablesUmatan.loc[race_id]
        # 的中判定
        hit = (table_1R['win_0'] == umaban[0]) * (table_1R['win_1'] == umaban[1])
        # 払い戻し合計額
        return_amount = hit * table_1R['return'] * amount / 100
        return 1, amount, return_amount

    def bet_umatan_box(self, race_id: str, umaban: list, amount: float):
        """
        馬単をBOX馬券で賭ける場合の関数。
        """
        n_bets = 0
        bet_amount = 0
        return_amount = 0
        for pair in permutations(umaban, 2):
            n_bets_single, bet_amount_single, return_amount_single \
                = self._bet_umatan(race_id, list(pair), amount)
            # 賭ける枚数
            n_bets += n_bets_single
            # 賭けた合計額
            bet_amount += bet_amount_single
            # 払い戻し合計額
            return_amount += return_amount_single
        return n_bets, bet_amount, return_amount

    def bet_wide_box(self, race_id: str, umaban: list, amount: float):
        """
        ワイドをBOX馬券で賭ける関数。1枚のみ賭ける場合もこの関数を使う。
        """
        # 賭ける枚数
        n_bets = comb(len(umaban), 2)
        # 賭けた合計額
        bet_amount = n_bets * amount
        # 賭けるレースidに絞ったワイド払い戻し表
        table_1R = self.__returnTablesWide.loc[race_id]
        # 的中判定
        hits = table_1R['win_0'].isin(umaban) * table_1R['win_1'].isin(umaban)
        # 払い戻し合計額
        return_amount = sum(
            hits * table_1R['return'] * amount / 100
        )
        return n_bets, bet_amount, return_amount

    def bet_sanrenpuku_box(self, race_id: str, umaban: list, amount: float):
        """
        三連複BOX馬券。1枚のみ買いたい場合もこの関数を使う。
        """
        # 賭ける枚数
        n_bets = comb(len(umaban), 3)
        # 賭けた合計額
        bet_amount = n_bets * amount
        # 賭けるレースidに絞った三連複払い戻し表
        table_1R = self.__returnTablesSanrenpuku.loc[race_id]
        # 的中判定
        hit = set(table_1R[['win_0', 'win_1', 'win_2']]).issubset(set(umaban))
        # 払い戻し合計額
        return_amount = hit * table_1R['return'] * amount / 100
        return n_bets, bet_amount, return_amount

    def _bet_sanrentan(self, race_id: str, umaban: list, amount: float):
        """
        三連単を一枚のみ賭ける場合の関数。umabanは[1着予想, 2着予想, 3着予想]の形で馬番を入れる。
        """
        #len(umaban) != 3の時の例外処理
        # 賭けるレースidに絞った三連単払い戻し表
        table_1R = self.__returnTablesSanrentan.loc[race_id]
        # 的中判定
        hit = (table_1R['win_0'] == umaban[0]) * (table_1R['win_1'] == umaban[1]) \
            * (table_1R['win_2'] == umaban[2])
        # 払い戻し合計額
        return_amount = hit * table_1R['return'] * amount / 100
        return 1, amount, return_amount

    def bet_sanrentan_box(self, race_id: str, umaban: list, amount: float):
        """
        三連単をBOX馬券で賭ける場合の関数。
        """
        n_bets = 0
        bet_amount = 0
        return_amount = 0
        for pair in permutations(umaban, 3):
            n_bets_single, bet_amount_single, return_amount_single \
                = self._bet_sanrentan(race_id, list(pair), amount)
            # 賭ける枚数
            n_bets += n_bets_single
            # 賭けた合計額
            bet_amount += bet_amount_single
            # 払い戻し合計額
            return_amount += return_amount_single
        return n_bets, bet_amount, return_amount

    def others(self, race_id: str, umaban: list, amount: float):
        """
        その他、フォーメーション馬券や流し馬券の定義
        """
        pass
