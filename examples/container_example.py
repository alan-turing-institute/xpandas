import pandas as pd
import numpy as np
from xpandas.data_container import XSeries, XDataFrame

n = 1000

xseries = XSeries([
        pd.Series(np.random.normal(size=500))
    ] * n)

xdataframe = XDataFrame({
    'gender': XSeries(np.random.binomial(1, 0.7, n)),
    'age': XSeries(np.random.poisson(25, n)),
    'series': xseries
})