import chess.pgn
import pandas as pd
import numpy as np

def separateChessMoves(chessString):
    span = 3
    liste_coup = chessString.split(" ")
    liste_trie = [" ".join(liste_coup[i:i + span]) for i in range(0, len(liste_coup), span)]
    white_moves = []
    black_moves = []

    for move in liste_trie:
        move_divise = move.split(" ")
        white_moves.append(move_divise[1])

        if len(move_divise) < 3:
            break

        if move_divise[2] != "1-0" and move_divise[2] != "0-1":
            black_moves.append(move_divise[2])
    return white_moves, black_moves


def find_castle(chessString):
    (white_moves, black_moves) = separateChessMoves(chessString)
    white_castle = 0
    black_castle = 0

    for move in white_moves:
        if move == "O-O":
            white_castle = 1
            break
        elif move == "O-O-O":
            white_castle = 2
            break

    for move in black_moves:
        if move == "O-O":
            black_castle = 1
        elif move == "O-O-O":
            black_castle = 2

    return (white_castle, black_castle)

def extract_from_pgn(file):
    data = []
    while True:
        chess_game = chess.pgn.read_game(file)
        if chess_game is None:
            break
        white_elo = chess_game.headers["WhiteElo"]
        black_elo = chess_game.headers["BlackElo"]
        game_string = str(chess_game.mainline_moves())
        castling_tuple = find_castle(game_string)
        white_short_castle = 0
        white_long_castle = 0
        white_castle = 0
        black_short_castle = 0
        black_long_castle = 0
        black_castle = 0

        #For white
        if castling_tuple[0] == 1:
            white_castle = 1
            white_short_castle = 1

        elif castling_tuple[0] == 2:
            white_castle = 1
            white_long_castle = 1

        #For black

        if castling_tuple[1] == 1:
            black_castle = 1
            black_short_castle = 1

        elif castling_tuple[1] == 2:
            black_castle = 1
            black_long_castle = 1

        data.append([white_elo, black_elo, white_castle, black_castle , white_short_castle, white_long_castle,
                 black_short_castle, black_long_castle])

    df = pd.DataFrame(data, columns=["White elo", "Black elo", "White castle", "Black castle", "white short",
                                     "White long", "black short", "black long"])

    return df


def create_castle_df(df, output = "castle.pkl"):
    new_df = []
    for index, row in df.iterrows():

        # For White
        player_elo = int(row["White elo"])
        castle = int(row["White castle"])
        new_df.append((player_elo, castle))

        #For black
        player_elo = int(row["Black elo"])
        castle = int(row["Black castle"])
        new_df.append((player_elo, castle))

    castle_df = pd.DataFrame(new_df, columns=["Player elo", "Castle"])
    castle_df.to_pickle(output)
    return castle_df


def df_from_png(input_file, output_file = ""):
    pgn = open(input_file)
    df = extract_from_pgn(pgn)

    if output_file != "":
        df.to_pickle(output_file)

    return df



if __name__ == "__main__":
    chess_string = "1. d4 d5 2. e4 e6 3. e5 Nc6 4. Nf3 Bb4+ 5. c3 Ba5 6. b4 Bb6 7. a4 a5 8. b5 Nce7 9. Bd3 Nh6 10. Bg5 Nhf5 11. O-O h6 12. Bc1 c5 13. Ba3 cxd4 14. Bxf5 Nxf5 15. cxd4 Qc7 16. g4 Ne7 17. Bd6 Qd7 18. Nc3 O-O 19. Rc1 Bc7 20. b6 Bxd6 21. exd6 Qxd6 22. Nb5 Qxb6 23. Ne5 f6 24. Nd3 e5 25. dxe5 fxe5 26. Nxe5 Nc6 27. Qxd5+ Kh7 28. Nxc6 bxc6 29. Rxc6 Qb7 30. Rd1 Bxg4 31. Rxh6+ gxh6 32. Qxb7+ Kg8 33. Rd6 Rae8 34. Rg6+ Kh8 35. Qg7# 1-0"
    (white_move, black_move) = separateChessMoves(chess_string)
    print(white_move)
    print(black_move)
    print(find_castle(chess_string))
