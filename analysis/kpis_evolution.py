import pandas as pd
import numpy as np


def kpi_evolution(df: pd.DataFrame):
    results = {}
    df_2015 = df[df['anyo'] == 2015]
    df_2018 = df[df['anyo'] == 2018]
    variables = df.columns[4:13]
    for var in variables:
        var_2015 = var + '_2015'
        var_2018 = var + '_2018'
        df_2015_var = df_2015[['nom_barrio', var]]
        df_2015_var = df_2015_var.rename(columns={var: var_2015})
        df_2018_var = df_2018[['nom_barrio', var]]
        df_2018_var = df_2018_var.rename(columns={var: var_2018})
        df_diff = pd.merge(df_2015_var, df_2018_var, on='nom_barrio',
                           how='inner')

        df_diff['diff'] = np.where(df_diff[var_2015] <= df_diff[var_2018],
                                   df_diff[var_2018] - df_diff[var_2015],
                                   df_diff[var_2015] - df_diff[var_2018])

        df_diff['diff_perc'] = np.round(df_diff['diff'] / df_diff[var_2015], 3)

        df_diff['evolution'] = np.where(
            df_diff[var_2015] <= df_diff[var_2018],
            '+' + df_diff['diff_perc'].astype(str) + '%',
            '-' + df_diff['diff_perc'].astype(str) + '%'
        )
        df_diff = df_diff.sort_values(by='diff_perc', ascending=False)
        results[var] = df_diff[['nom_barrio', 'evolution']]

    return results







