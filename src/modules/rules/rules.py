from src.modules.rules.board import Board as Bd
from src.modules.player.player import User, Random
from src.modules.view.view import output_console as oc

def set_usr():
    return


def set_difficulty():
    return


def start_game(b_player, w_player):
    board = Bd()
    black = b_player
    white = w_player
    while True:
        now_legal, alt_legal, turn = board.get_candidate()

        if turn is None:
            # ゲーム終了
            break

        oc(board)

        if now_legal == 0:
            # TODO パスになる旨記載
            now_legal = alt_legal

        if turn == 0:
            board.put_disc(black.judge(board))
        else:
            board.put_disc(white.judge(board))
    
    print(board.disc_count(agg="bw"))


if __name__ == '__main__':
    start_game(User, Random)