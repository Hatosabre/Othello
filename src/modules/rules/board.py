#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Othello Board Module.

このモジュールは、オセロのボード上の情報を保持するためのクラスのみを記載しています
ボードは8×8の64マスで、左上から右上、左下、右下の順に0～63の番号が振られている。
初期マスは、(28, 35)が黒、(27, 36)が白で開始する

TODO:
    ボードの大きさは正方形は変えないが、8を変えられるようにはしたい
    初期マスも固定しないものを考える

"""
import src.modules.const.const as cst

cst.DEFAULT_FIRST_BLACK_PLACE = 0x0000000810000000
cst.DEFAULT_FIRST_WHITE_PLACE = 0x0000001008000000
cst.BLACK_TURN = 0
cst.WHITE_TURN = 1
cst.DEFAULT_FIRST_TURN = cst.BLACK_TURN


class Board:
    """オセロボード情報保持用クラス
    """
    class InvalidArrangeException(ValueError):
        """
        正しくない初期値が引数に入った場合に投げられるエラー
        """
        def __init__(self, b_err, w_err, turn_err):
            if b_err:
                print("黒駒の引数が誤っています。0～0xffffffffffffffffの間で入力してください")
            if w_err:
                print("白駒の引数が誤っています。0～0xffffffffffffffffの間で入力してください")
            if turn_err:
                print("黒番なら　0　を, 白番なら　1　を入力してください")
            return

    class InvalidPutDiscException(ValueError):
        pass

    def __init__(self, b_disc=cst.DEFAULT_FIRST_BLACK_PLACE,
                       w_disc=cst.DEFAULT_FIRST_WHITE_PLACE,
                       turn  =cst.DEFAULT_FIRST_TURN):
        """
        初期設定

        Args:
            b_disc: 初期黒駒マス
            w_disc: 初期白駒マス
            turn: 初期ターンユーザ
        """

        # 異常値の例外処理
        # 各駒配置は0～63盤のマス×存在有無のため,
        # 0(1マスも埋まっていない)～2**64-1(全て埋まっている)の間
        is_b_disc_err = not (0 <= b_disc <= 2 ** 64 - 1)
        is_w_disc_err = not (0 <= w_disc <= 2 ** 64 - 1)
        is_turn_err = not (turn in (0, 1))
        if is_b_disc_err or is_w_disc_err or is_turn_err:
            raise self.InvalidArrangeException(is_b_disc_err,
                                               is_w_disc_err,
                                               is_turn_err)

        self.b_disc = b_disc  # init black disc
        self.w_disc = w_disc  # init white disc

        self.turn = turn  # 0 is black, 1 is white

        self.put = []  # put history
        self.rev = []  # reverse history

    def get_disc(self):
        """各色の駒の場所を取得
        
        Returns:
            [(int, int)] -- [黒駒,白駒の場所]
        """
        return self.b_disc, self.w_disc

    def get_turn(self):
        """

        Returns:
            [int] -- [現在のターンユーザ 0 is black, 1 is white]

        """
        return self.turn

    def __reverse(self, site):
        """駒が置かれたときにひっくり返される駒を出力する
        
        Arguments:
            site {int} -- [駒の置く場所]
                Example:
                    左から2番目、上から3番目のマスに置く場合は、2^(2 + (3-1)*8 - 1)
                    左から6番目、上から5番目のマスに置く場合は、2^(6 + (5-1)*8 - 1)
        
        Returns:
            [int] -- [ひっくり返される駒の場所]
                Example:
                    左から2番目、上から3番目と、左から2番目、上から4番目がひっくり返される場合、
                    2^(2 + (3-1)*8 - 1) + 2^(2 + (4-1)*8 - 1)が返る
        """

        def reverse_by_left(mask, direct):
            """駒が置かれたときにひっくり返される駒を出力する.(左シフトver)

            bit演算のマイナスシフトが出来ないため、右シフト用の関数と合わせて作成する
            
            Arguments:
                mask {int} -- [相手が既に打っている場合、反転しようがないマス]
                direct {int} -- [シフト数]
            
            Returns:
                [int] -- [ひっくり返される駒の場所]
            """

            # 結果保管用変数
            rev = 0

            # 置いたマスの隣(direct方向)に違う色の駒が置かれているか
            is_exist_disc = ~(p_disc | mask) & (site << direct)

            if is_exist_disc:
                for _ in range(8):

                    # さらに隣に移動
                    is_exist_disc <<= direct
                    if is_exist_disc & mask:
                        # 進んだ先に置いた駒の色と同じ駒がなかった
                        # もしくは、空マスがあったため
                        # 変換不能
                        break
                    elif is_exist_disc & p_disc:

                        # 進んだ先に置いた駒の色と同じ駒があったため
                        # 変換可能
                        rev |= is_exist_disc >> direct
                        break
                    else:
                        # 進んだ先に置いた駒と違う色の駒があり、その隣にもまだ駒が存在するため
                        # ひっくり返す候補を加えて継続
                        is_exist_disc |= is_exist_disc >> direct

            return rev

        def reverse_by_right(mask, direct):
            """駒が置かれたときにひっくり返される駒を出力する.(右シフトver)

            bit演算のマイナスシフトが出来ないため、左シフト用の関数と合わせて作成する
            
            Arguments:
                mask {int} -- [相手が既に打っている場合、反転しようがないマス]
                direct {int} -- [シフト数]
            
            Returns:
                [int] -- [ひっくり返される駒の場所]
            """
            rev = 0
            is_exist_disc = ~(p_disc | mask) & (site >> direct)

            if is_exist_disc:
                for _ in range(8):
                    is_exist_disc >>= direct
                    if is_exist_disc & mask:
                        break
                    elif is_exist_disc & p_disc:
                        rev |= is_exist_disc << direct
                        break
                    else:
                        is_exist_disc |= is_exist_disc << direct

            return rev

        # 白のターンの場合は、
        # p_disc(playerの駒)に白駒配置を
        # o_disc(opponentの駒)に黒駒配置を設定
        # 黒のターンなら逆
        if self.turn:
            p_disc = self.w_disc
            o_disc = self.b_disc
        else:
            p_disc = self.b_disc
            o_disc = self.w_disc

        # この場所に置いた駒と違う色があった場合はひっくり返らない
        # 横方向なら一番左の列と一番右の列・・・mask_r
        # 縦方向なら一番上の行と一番下の行・・・mask_c
        # 斜方向なら一番上・下行、右・左列・・・mask_s
        mask_r = ~(p_disc | o_disc & 0x7e7e7e7e7e7e7e7e)
        mask_c = ~(p_disc | o_disc & 0x00ffffffffffff00)
        mask_s = ~(p_disc | o_disc & 0x007e7e7e7e7e7e00)

        revs = 0

        revs |= reverse_by_left(mask_r, 1)
        revs |= reverse_by_left(mask_c, 8)
        revs |= reverse_by_left(mask_s, 7)
        revs |= reverse_by_left(mask_s, 9)
        revs |= reverse_by_right(mask_r, 1)
        revs |= reverse_by_right(mask_c, 8)
        revs |= reverse_by_right(mask_s, 7)
        revs |= reverse_by_right(mask_s, 9)

        return revs

    def put_disc(self, place):
        """駒を置いて、反転させる
        
        Arguments:
            place {int} -- [置き場]
        
        Raises:
            Exception: [反転しなかった場合は、入力値が間違っている]
        """
        if (self.b_disc & place) or (self.w_disc & place):
            raise self.InvalidPutDiscException()

        rev = self.__reverse(place)
        if rev == 0:
            raise self.InvalidPutDiscException()

        self.put.append(place)
        self.rev.append(rev)

        if self.turn:
            self.w_disc ^= rev ^ place
            self.b_disc ^= rev
        else:
            self.b_disc ^= rev ^ place
            self.w_disc ^= rev

        return

    def __legal(self):
        """置ける場所を確認する
        
        Returns:
            [int] -- [置ける場所]
        """

        def legal_by_left(mask, direct):
            """置ける場所を確認する(左シフトver)

            ひっくり返す方向は、縦・横・斜め(×2)の4種類ある。
            各方向にプレイヤーの駒をシフトして、(各方向に対して)端ではない相手のマスに重なったら、フラグをつける
            逆に自分のマスに重なったらフラグをなくす。最終的に空マスにぶつかった際、フラグがついていれば候補値になる
            
            bit演算のマイナスシフトが出来ないため、左シフト用の関数と合わせて作成する
            
            Arguments:
                p_disc {[int]} -- [手番プレイヤーの持ち駒]
                mask {[int]} -- [間にひっくり返される駒があることを確認するマスク]
                blank {[type]} -- [空マス]
                direct {[type]} -- [シフト数]
            
            Returns:
                [int] -- [置ける場所]
            """
            tmp = mask & (p_disc << direct)
            for _ in range(5):
                tmp |= mask & (tmp << direct)

            return blank & (tmp << direct)

        def legal_by_right(mask, direct):
            """置ける場所を確認する(右シフトver)

            ひっくり返す方向は、縦・横・斜め(×2)の4種類ある。
            各方向にプレイヤーの駒をシフトして、(各方向に対して)端ではない相手のマスに重なったら、フラグをつける
            逆に自分のマスに重なったらフラグをなくす。最終的に空マスにぶつかった際、フラグがついていれば候補値になる
            
            bit演算のマイナスシフトが出来ないため、左シフト用の関数と合わせて作成する
            
            Arguments:
                p_disc {[int]} -- [手番プレイヤーの持ち駒]
                mask {[int]} -- [間にひっくり返される駒があることを確認するマスク]
                blank {[type]} -- [空マス]
                direct {[type]} -- [シフト数]
            
            Returns:
                [int] -- [置ける場所]
            """
            tmp = mask & (p_disc >> direct)
            for _ in range(5):
                tmp |= mask & (tmp >> direct)

            return blank & (tmp >> direct)

        if self.turn:
            p_disc = self.w_disc
            o_disc = self.b_disc
        else:
            p_disc = self.b_disc
            o_disc = self.w_disc

        blank = ~(p_disc | o_disc)

        mask_r = o_disc & 0x7e7e7e7e7e7e7e7e
        mask_c = o_disc & 0x00ffffffffffff00
        mask_s = o_disc & 0x007e7e7e7e7e7e00

        legal = 0

        legal |= legal_by_left(mask_r, 1)
        legal |= legal_by_left(mask_c, 8)
        legal |= legal_by_left(mask_s, 7)
        legal |= legal_by_left(mask_s, 9)
        legal |= legal_by_right(mask_r, 1)
        legal |= legal_by_right(mask_c, 8)
        legal |= legal_by_right(mask_s, 7)
        legal |= legal_by_right(mask_s, 9)

        return legal

    def get_candidate(self):
        """候補値を取得
        
        Returns:
            [int, int or boolean, 0 or 1 or None] 
                -- [現ターンに置ける候補数，現ターンの候補数が0でないならばFalse/0ならば次のユーザの候補数, 現在のターン]
        """
        legal = self.__legal()

        if legal == 0:
            self.put.append(0)
            self.rev.append(0)
            self.turn ^= 1

            legal = self.__legal()

            if legal == 0:
                return 0, 0, None

            return 0, legal, self.turn

        return legal, False, self.turn

    def backward(self):
        """ターンを戻す
        """
        if self.put[-1] != 0:
            self.turn ^= 1
            put = self.put[-1]
            rev = self.rev[-1]
            self.put = self.put[:-1]
            self.rev = self.rev[:-1]
        else:
            put = self.put[-2]
            rev = self.rev[-2]
            self.put = self.put[:-2]
            self.rev = self.rev[:-2]

        if self.turn:
            self.w_disc ^= rev ^ put
            self.b_disc ^= rev
        else:
            self.b_disc ^= rev ^ put
            self.w_disc ^= rev

    # <===========================以下各種統計取得用関数==================================>

    def disc_count(self, agg):
        if agg == "b":
            cnt = 0
            for i in range(64):
                if self.b_disc & (1 << i):
                    cnt += 1
            return cnt

        elif agg == "w":
            cnt = 0
            for i in range(64):
                if self.w_disc & (1 << i):
                    cnt += 1
            return cnt

        elif agg == "bw":
            b_cnt = 0
            w_cnt = 0
            for i in range(64):
                if self.b_disc & (1 << i):
                    b_cnt += 1
                if self.w_disc & (1 << i):
                    w_cnt += 1
            return b_cnt, w_cnt
