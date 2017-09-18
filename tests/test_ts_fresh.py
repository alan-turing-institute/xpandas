import numpy as np
import pandas as pd

from ..transformers.data_container import MultiSeries, MultiDataFrame
from ..transformers.transformers.pipeline_transformer import PipeLineChain
from ..transformers.transformers.series_transformers import TsFreshSeriesTransformer, TimeSeriesWindowTransformer
from ..transformers.transformers.transformer import DataFrameTransformer


def test_ts_fresh_series():
    series = MultiSeries([
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

    assert type(transformed) == MultiDataFrame


def test_ts_fresh_df():
    s1 = MultiSeries([
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10))
    ], name='X')
    s2 = MultiSeries([
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10)),
        pd.Series(np.random.uniform(0, 100, 10))
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


def test_ts_fresh_chain():
    s1 = MultiSeries([
        pd.Series(np.random.normal(0, 1, 20))
        for _ in range(10)
    ], name='X')

    pipe = PipeLineChain([
        ('mean shift', TimeSeriesWindowTransformer()),
        ('ts fresh step', TsFreshSeriesTransformer())
    ])

    pipe.fit(s1)
    transformed_df = pipe.transform(s1)

    print(transformed_df.head())

    assert type(transformed_df) == MultiDataFrame
