import pandas as pd
import chess_fun
import matplotlib.pyplot as plt
import numpy as np
import fonctionsUtiles as utile

pd.set_option('display.max_columns',None)


#df = pd.read_pickle("TerribleVillageois.pkl")
df = chess_fun.df_from_png("D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn")

df_castle = chess_fun.create_castle_df(df)

data, matrice = utile.cut_dataframe(df_castle,"Player elo", 100)


plt.bar(matrice,data["Castle"])

plt.show()

# pgn = open("D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn")
# df = chess_fun.extract_from_pgn(pgn)
# df.to_pickle("TerribleVillageois.pkl")


#
# print(df["White castle"].sum())
# print(df["white short"].sum())
# print(df["White long"].sum())
# D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn