import pandas as pd
import numpy as np

def cut_dataframe(df, col_name, step):
    min_value = df[col_name].min()
    max_value = df[col_name].max()
    matrice = np.arange(min_value, max_value, step)

    df_coupe = df.groupby(pd.cut(df[col_name], matrice)).mean()

    matrice_string = []
    for i in range(len(matrice)-1):
        this_val = matrice[i]
        next_val = matrice[i+1]
        interval_string = "De {} à {}".format(this_val, next_val)
        print(interval_string)
        matrice_string.append(interval_string)

    return df_coupe, matrice_string