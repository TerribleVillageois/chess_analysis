import chess.pgn
import pandas as pd
import chess_fun as chess_fun

def df_from_png(input_file, output_file = ""):
    pgn = open(input_file)
    df = chess_fun.extract_from_pgn(pgn)

    if output_file != "":
        df.to_pickle(output_file)

    return df

# D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn