import random


class Player:
    @staticmethod
    def judge(board):
        return


class User(Player):
    @staticmethod
    def judge(board):
        legal, _, _ = board.get_candidate()
        print(bin(legal))
        input_cell_num = int(input())
        return 1 << input_cell_num


class Random(Player):

    @staticmethod
    def judge(board):
        legal, _, _ = board.get_candidate()
        cand = []
        for i in range(64):
            if legal & (1 << i):
                cand.append(i)
        
        put = random.choice(cand)
        return 1 << put
