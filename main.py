import pandas as pd
import chess_fun
import matplotlib.pyplot as plt
import numpy as np
import fonctionsUtiles as utile
import seaborn as sns

pd.set_option('display.max_columns', None)

df = pd.read_pickle("Lichess_Test.pkl")
#df = chess_fun.df_from_png("D:/lichessGames/lichess_db_standard_rated_2021-12.pgn", "Lichess_Test.pkl", 30000)

df_Blitz = df[df["Event type"] == "Rated Bullet game"]
df_Rapid = df[df["Event type"] == "Rated Rapid game"]

df_castle_Blitz = chess_fun.create_castle_df(df_Blitz)
df_castle_Rapid = chess_fun.create_castle_df(df_Rapid)

df_castle = chess_fun.create_castle_df(df)

print(df_castle.head())
import statsmodels.api as sm

y = df_castle['Castle']
X = sm.add_constant(df_castle[['Player elo', "Rating diff"]])

logit_model = sm.Logit(y, X)
result = logit_model.fit()
print(result.summary())


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.5, random_state = 0)
logreg = LogisticRegression()
logreg.fit(X_train,y_train)

y_pred = logreg.predict(X_test)
print("La prédiction est correct à {:.2f}".format(logreg.score(X_test,y_test)))


# data, matrice = utile.cut_dataframe(df_castle,"Player elo", 100)
# data2, matrice2 = utile.cut_dataframe(df_castle_Rapid,"Player elo", 500, np.arange(300, 2500, 100))
# data3, matrice3 = utile.cut_dataframe(df_castle_Blitz,"Player elo", 500, np.arange(300, 2500, 100))
#
# plt.plot(matrice,data["Castle"],'-+')
# plt.plot(matrice2,data2["Castle"],'-+', label = "Rapid")
# plt.plot(matrice3,data3["Castle"],'-+', label = "Blitz")
# # sns.catplot(x = matrice, y = data["Castle"],hue = data["Event type"])
# #
# #
# plt.legend()
# plt.show()
#
# print(df.describe())

# pgn = open("D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn")
# df = chess_fun.extract_from_pgn(pgn)
# df.to_pickle("TerribleVillageois.pkl")


#
# print(df["White castle"].sum())
# print(df["white short"].sum())
# print(df["White long"].sum())
# D:/lichessGames/lichess_TerribleVillageois_2021-12-20.pgn
