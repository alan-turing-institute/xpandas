import numpy as np
import pandas as pd

from ..xpandas.data_container import XSeries, XDataFrame
from ..xpandas.transformers.pipeline_transformer import PipeLineChain
from ..xpandas.transformers.series_transformers import TsFreshSeriesTransformer, TimeSeriesWindowTransformer
from ..xpandas.transformers.transformer import XDataFrameTransformer


def test_ts_fresh_series():
    series = XSeries([
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100)),
        pd.Series(np.random.uniform(0, 100, 100))
    ], name='Y')

    series = series
    # print(series.index)

    transformer = TsFreshSeriesTransformer()

    transformer.fit(series)
    transformed = transformer.transform(series)
    # print(transformed)

    assert type(transformed) == XDataFrame


def test_ts_fresh_df():
    s1 = XSeries([
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10))
    ], name='X')
    s2 = XSeries([
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10))
    ], name='Y')

    df = XDataFrame({
        'X': s1,
        'Y': s2
    })

    data_frame_transformer = XDataFrameTransformer(transformations={
        'X': TsFreshSeriesTransformer(),
        'Y': TsFreshSeriesTransformer()
    })

    data_frame_transformer.fit(df)
    transformed_df = data_frame_transformer.transform(df)

    assert type(transformed_df) == XDataFrame


def test_ts_fresh_chain():
    s1 = XSeries([
        pd.Series(np.random.normal(0, 1, 20))
        for _ in range(10)
    ], name='X')

    pipe = PipeLineChain([
        ('mean shift', TimeSeriesWindowTransformer()),
        ('ts fresh step', TsFreshSeriesTransformer())
    ])

    pipe.fit(s1)
    transformed_df = pipe.transform(s1)

    # print(transformed_df.head())

    assert type(transformed_df) == XDataFrame
