import random
from src.modules.rules.board import Board as Bd

class Player:
    def judge(self, board):
        return


class User(Player):
    def judge(self, board):
        legal, _, _ = board.get_candidate()
        input_cell_num = int(input())
        return 1 << input_cell_num


class Random(Player):

    def judge(self, board):
        legal, _, _ = board.get_candidate()
        cand = []
        for i in range(64):
            if legal & (1 << i):
                cand.append(i)
        
        put = random.choice(cand)
        return 1 << put


class AlphaBeta(Player):
    def __init__(self, depth):
        self.depth = depth

    def judge(self, board):

        def __alpha(bd, depth):
            b, w = bd.get_disc()
            t = bd.get_turn()
            new_bd = Bd(b_disc=b, w_disc=w, turn=t)
            values = dict()
            jdg = new_bd.get_candidate(is_pass=False)
            if jdg == 0:
                new_bd.turn_pass()
                if depth == 0:
                    value = __eval(new_bd)
                else:
                    value = __alpha(new_bd, depth-1)
                return value
            else:
                for i in range(64):
                    if jdg & (1 << i):
                        new_bd.put_disc(1 << i)
                        if depth == 0:
                            values[i] = __eval(new_bd)
                        else:
                            values[i] = __alpha(new_bd, depth-1)
                            new_bd.backward()

            if t == board.get_turn():
                if depth == self.depth:
                    return max(values, key=values.get)
                return max(values.values())

            else:
                return min(values.values())

        def __eval(bd):
            b, w = bd.get_disc()
            t = bd.get_turn()
            jdg = bd.get_candidate(is_pass=False)

            p_cnt = 0
            o_cnt = 0
            p_corner_cnt = 0
            o_corner_cnt = 0
            p_cross_cnt = 0
            o_cross_cnt = 0
            p_jdg_cnt = 0
            o_jdg_cnt_d = []

            if t:
                p = w
                o = b
            else:
                p = b
                o = w
            for i in range(64):
                mask = 1 << i
                if p & mask:
                    p_cnt += 1
                    if i in (0, 7, 56, 63):
                        p_corner_cnt += 1
                    elif i in (1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62):
                        p_cross_cnt += 1

                if o & mask:
                    o_cnt += 1
                    if i in (0, 7, 56, 63):
                        o_corner_cnt += 1
                    elif i in (1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62):
                        o_cross_cnt += 1

                if jdg & mask:
                    p_jdg_cnt += 1
                    bd.put_disc(mask)
                    o_jdg = bd.get_candidate(is_pass=False)
                    tmp = 0
                    for j in range(64):
                        if o_jdg & (1 << j):
                            tmp += 1
                    o_jdg_cnt_d.append(tmp)
                    bd.backward()

            o_jdg_cnt = max(o_jdg_cnt_d)
            diff_cnt = p_cnt - o_cnt

            print(
                  # bin(p), bin(o),
                  p_cnt, o_cnt,
                  p_corner_cnt, o_corner_cnt,
                  p_cross_cnt, o_cross_cnt,
                  p_jdg_cnt, o_jdg_cnt,
                  diff_cnt)

            return Random

        # put = __alpha(board, self.depth)
        b, w = board.get_disc()
        t = board.get_turn()
        b = Bd(b_disc=b, w_disc=w, turn=t)
        r = __eval(b)
        return r.judge(r, board)


