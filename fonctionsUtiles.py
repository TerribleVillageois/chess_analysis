import seaborn as sns
import pandas as pd
import numpy as np
sns.set_theme()

def cut_dataframe(df, col_name, step = 0, matrice = []):
    min_value = df[col_name].min()
    max_value = df[col_name].max()
    if matrice == []:
        matrice = np.arange(min_value, max_value, step)

    df_coupe = df.groupby(pd.cut(df[col_name], matrice, right=False)).mean()

    matrice_string = []
    for i in range(len(matrice)-1):
        this_val = matrice[i]
        next_val = matrice[i+1]
        interval_string = "[{},{}[".format(this_val, next_val)
        matrice_string.append(interval_string)

    return df_coupe, matrice_string



