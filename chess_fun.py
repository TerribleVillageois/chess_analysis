import chess.pgn
import pandas as pd
import numpy as np
import re


def separateChessMoves(chess_game_string, regex="[a-h][1-8]|[a-zA-Z][a-h][1-8]|[a-zA-Z][a-zA-Z][a-h][1-8]|O-O-O|O-O"):
    """Find all chess moves in a text and seperates the moves done by white and the moves done by black

    Parameters
    ----------
    chess_game_string : str
        The algebraic notation of a chess game returned by the chess parser
    Regex : str
        the regular expression used to only keep the moves from the full algebraic notation

    Returns
    -------
    Tuple
        a tuple that contains all the white moves and the black moves in a string
    """
    liste_moves = re.findall(regex, chess_game_string)
    white_moves = []
    black_moves = []
    for i, e in enumerate(liste_moves):
        if i % 2 == 0:
            white_moves.append(e)
        else:
            black_moves.append(e)

    return white_moves, black_moves


def find_castle(chessString):
    """Find if one or both player have castle in a game

    Parameters
    ----------
    chess_game_string : str
        The algebraic notation of a chess game returned by the chess parser

    Returns
    -------
    Tuple
        a tuple of bools that tells if white and black have castle in the game
    """
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


def extract_from_pgn(chess_file, max_value=9999999999999999999999999, print_compteur=False):
    """Create a dataframe that contains the information we need for our analysis from a pgn file that contains an arbitrate number of games

    Parameters
    ----------
    chess_file : file
        A pgn file that contains one or multiple games

    print_compteur : bool
        A bool that allow to print the progression of the function. It prints the number of games parsed each 1000 games.

    Returns
    -------
    dataframe
        a dataframe that contains the information we need about each game like the white elo and the black elo and if players have castled in the game.
    """
    data = []
    compteur = 0
    while compteur != max_value:
        chess_game = chess.pgn.read_game(chess_file)
        compteur += 1
        if chess_game is None:
            break
        white_elo = int(chess_game.headers["WhiteElo"])
        black_elo = int(chess_game.headers["BlackElo"])
        white_rating_diff = white_elo - black_elo
        black_rating_diff = black_elo - white_elo
        event_type = chess_game.headers["Event"]
        game_string = str(chess_game.mainline_moves())
        castling_tuple = find_castle(game_string)
        white_short_castle = 0
        white_long_castle = 0
        white_castle = 0
        black_short_castle = 0
        black_long_castle = 0
        black_castle = 0

        # For white
        if castling_tuple[0] == 1:
            white_castle = 1
            white_short_castle = 1

        elif castling_tuple[0] == 2:
            white_castle = 1
            white_long_castle = 1

        # For black

        if castling_tuple[1] == 1:
            black_castle = 1
            black_short_castle = 1

        elif castling_tuple[1] == 2:
            black_castle = 1
            black_long_castle = 1

        if compteur % 1000 == 0 and print_compteur == True:
            print(compteur)

        data.append([white_elo, black_elo, white_castle, black_castle, white_short_castle, white_long_castle,
                     black_short_castle, black_long_castle, white_rating_diff, black_rating_diff, event_type])

    df = pd.DataFrame(data, columns=["White elo", "Black elo", "White castle", "Black castle", "white short",
                                     "White long", "black short", "black long", "White rating diff",
                                     "Black rating diff",
                                     "Event type"])

    return df


def create_castle_df(df, output="castle.pkl"):
    """Find all chess moves in a text and seperates the moves done by white and the moves done by black

    Parameters
    ----------
    df : dataframe
        A dataframe that contains all the informations extracted from a pgn file
    output : str
        An optional parameters that allow the user to save the dataframe in a pickle object.

    Returns
    -------
    dataframe
        a dataframe that have seperated white games and black games and collaps the information about short and long castle.
    """
    new_df = []
    for index, row in df.iterrows():
        # For White
        player_elo = int(row["White elo"])
        castle = int(row["White castle"])
        event_type = row["Event type"]
        rating_diff = row["White rating diff"]
        new_df.append((player_elo, castle, rating_diff, event_type))

        # For black
        player_elo = int(row["Black elo"])
        castle = int(row["Black castle"])
        event_type = row["Event type"]
        rating_diff = row["Black rating diff"]
        new_df.append((player_elo, castle, rating_diff, event_type))

    castle_df = pd.DataFrame(new_df, columns=["Player elo", "Castle", "Rating diff", "Event type"])
    castle_df.to_pickle(output)
    return castle_df


def df_from_png(input_file, output_file="", limit=0):
    pgn = open(input_file)
    df = extract_from_pgn(pgn, limit)

    if output_file != "":
        df.to_pickle(output_file)

    return df


if __name__ == "__main__":
    chess_string = "1. d4 d5 2. e4 e6 3. e5 Nc6 4. Nf3 Bb4+ 5. c3 Ba5 6. b4 Bb6 7. a4 a5 8. b5 Nce7 9. Bd3 Nh6 10. Bg5 Nhf5 11. O-O h6 12. Bc1 c5 13. Ba3 cxd4 14. Bxf5 Nxf5 15. cxd4 Qc7 16. g4 Ne7 17. Bd6 Qd7 18. Nc3 O-O 19. Rc1 Bc7 20. b6 Bxd6 21. exd6 Qxd6 22. Nb5 Qxb6 23. Ne5 f6 24. Nd3 e5 25. dxe5 fxe5 26. Nxe5 Nc6 27. Qxd5+ Kh7 28. Nxc6 bxc6 29. Rxc6 Qb7 30. Rd1 Bxg4 31. Rxh6+ gxh6 32. Qxb7+ Kg8 33. Rd6 Rae8 34. Rg6+ Kh8 35. Qg7# 1-0"
    (white_move, black_move) = separateChessMoves(chess_string)
    print(white_move)
    print(black_move)
    print(find_castle(chess_string))
