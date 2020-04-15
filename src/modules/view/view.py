def output_console(board):
    legal, _, _ = board.get_candidate()
    b_disc, w_disc = board.get_disc()

    res = ""

    res += "-" * 38
    res += "\n"

    for i in range(8):
        for j in range(8):
            sub = i * 8 + j
            mask = 2 ** sub
            if j == 0:
                res += "|"

            if mask & b_disc:
                res += " ● |"
            elif mask & w_disc:
                res += " ○ |"
            elif mask & legal:
                res += " {} |".format(str(sub).zfill(2))
            else:
                res += " 　 |"

        res += "\n"
        res += "-"*38
        res += "\n"

    print(res)


