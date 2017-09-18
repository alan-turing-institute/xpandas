import numpy as np
import pandas as pd

from ..transformers.data_container import MultiSeries, MultiDataFrame
from ..transformers.transformers import DataFrameTransformer
from ..transformers.transformers.series_transformers import TsFreshSeriesTransformer


def test_ts_fresh_series():
    series = MultiSeries([
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100))
    ], name='Y')

    series = series[2:]
    # print(series.index)

    transformer = TsFreshSeriesTransformer()

    transformer.fit(series)
    transformed = transformer.transform(series)
    # print(transformed)

    assert type(transformed) == MultiDataFrame


def test_ts_fresh_df():
    s1 = MultiSeries([
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
    ], name='X')
    s2 = MultiSeries([
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
    ], name='Y')

    df = MultiDataFrame({
        'X': s1,
        'Y': s2
    })

    data_frame_transformer = DataFrameTransformer(transformations={
        'X': TsFreshSeriesTransformer(),
        'Y': TsFreshSeriesTransformer()
    })

    data_frame_transformer.fit(df)
    transformed_df = data_frame_transformer.transform(df)

    assert type(transformed_df) == MultiDataFrame
   