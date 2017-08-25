import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from src.data_container import CustomSeries, CustomDataFrame
from src.transformer import CustomTransformer, TimeSeriesTransformer
import pandas as pd
import numpy as np


def test_transformer_custom():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: series.mean())
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == CustomSeries
    assert s_transformed.data_type == np.float64


def test_transformer_custom_to_data_frame():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: {'mean': series.mean()})
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == CustomDataFrame


def test_transformer_custom_series_to_series():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = CustomTransformer(transform_function=lambda series: series + 1)
    series_transformer = series_transformer.fit()

    s_transformed = series_transformer.transform(s)

    assert type(s_transformed) == CustomSeries
    assert s_transformed.data_type == pd.Series


def test_transformer_series_transformer():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    series_transformer = TimeSeriesTransformer()
    series_transformer = series_transformer.fit()

    transformed_series = series_transformer.transform(s)

    assert type(transformed_series) == CustomDataFrame
