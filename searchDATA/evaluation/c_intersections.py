import plotly.express as px
import pandas as pd
import math
import numpy as np

#colors: https://plotly.com/python/discrete-color/

import plotly.io as pio
pio.kaleido.scope.mathjax = None

if __name__ == '__main__':

    data = pd.read_csv("results_csv/c_intersections.csv")

    r1_q = data.query("subset.str.contains('R1andW1')")
    #r1_q = data.query("subset.str.contains('W1notR2')")
    r1 = pd.DataFrame(r1_q)
    print(r1)


    median_per_set = r1.groupby('set')['amount'].agg(['median', 'min', 'max']).reset_index()
    median = pd.DataFrame(median_per_set)



    extra_group = r1.groupby('set')['amount']
    iqr = extra_group.apply(lambda x: np.percentile(x,75) - np.percentile(x,25))
    mad = extra_group.apply(lambda x: np.mean(np.abs(x-np.median(x))))

    df2 = pd.DataFrame({'set': iqr.index, 'IQR': iqr.values, 'MAD': mad.values})


    grouped_data = pd.merge(median_per_set, df2, on='set', how='left')
    print(grouped_data)













