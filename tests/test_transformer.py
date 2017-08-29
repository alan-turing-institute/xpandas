import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from src.data_container import MultiSeries, MultiDataFrame
from src.transformer import *
import pandas as pd
import numpy as np


def test_transformer_custom():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: series.mean())
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == MultiSeries
    assert s_transformed.data_type == np.float64


def test_transformer_custom_to_data_frame():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: {'mean': series.mean()})
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == MultiDataFrame


def test_transformer_custom_series_to_series():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: series + 1)
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == MultiSeries
    assert s_transformed.data_type == pd.Series


def test_transformer_series_transformer():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = TimeSeriesTransformer()
    series_transformer = series_transformer.fit()

    transformed_series = series_transformer.transform(s)

    assert type(transformed_series) == MultiDataFrame


def test_transformer_series_to_series_transformer():
    s = MultiSeries([
        pd.Series(np.random.normal(0, 10, 100)),
        pd.Series(np.random.uniform(-100, 100, 150)),
        pd.Series(np.random.random_integers(0, 500, 200))
    ])

    series_to_series_transformer = TimeSeriesWindowTransformer().fit()
    transformed_series = series_to_series_transformer.transform(s)

    assert series_to_series_transformer.transform_func(s[0]).equals(transformed_series[0])
    assert transformed_series.data_type == pd.Series
    assert type(transformed_series) == MultiSeries


def test_transformer_data_frame():
    s1 = MultiSeries([pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                       pd.Series([4, 5, 6], index=['d', 'e', 'g'])])
    s2 = MultiSeries([1, 2, 3])
    s3 = MultiSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = MultiSeries(['f', 's', 't'])

    df = MultiDataFrame({
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    data_frame_transformer = TimeSeriesTransformer().fit()
    try:
        data_frame_transformer.transform(df)
        assert False
    except:
        assert True

    s1 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=15))
    ])
    s2 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=10))
    ])
    s3 = MultiSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = MultiSeries(['f', 's', 't'])
    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    data_frame_transformer = TimeSeriesTransformer().fit()
    transformers_df = data_frame_transformer.transform(df)

    assert transformers_df.shape[1] == 6
