import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from ..xpandas.data_container import XDataFrame, XSeries
from ..xpandas.transformers import XSeriesTransformer, TimeSeriesTransformer, \
    TimeSeriesWindowTransformer, MeanSeriesTransformer, IdentityTransformer, \
    XDataFrameTransformer, PipeLineChain
import pandas as pd
import numpy as np


def test_naming():
    X = XSeries([
        pd.Series(np.random.normal(0, 1, 100), name='X')
    ])
    df = XDataFrame({
        'X': X
    })

    dataframe_transformer = XDataFrameTransformer({
        'X': [TimeSeriesTransformer()]
    })

    dataframe_transformer.fit(df)
    transformed_df = dataframe_transformer.transform(df)

    for col_name in transformed_df.columns:
        assert col_name.startswith('X_TimeSeriesTransformer')


def test_multiple_transformers_for_one_column():
    X = XSeries([
        pd.Series(np.random.normal(0, 1, 100), name='X')
    ])
    df = XDataFrame({
        'X': X
    })

    dataframe_transformer = XDataFrameTransformer({
        'X': [TimeSeriesTransformer(), IdentityTransformer(), MeanSeriesTransformer()]
    })

    dataframe_transformer.fit(df)
    transformed_df = dataframe_transformer.transform(df)

    for col_name in transformed_df.columns:
        assert col_name.startswith('X_TimeSeriesTransformer') or \
               col_name.startswith('X_IdentityTransformer') or \
               col_name.startswith('X_MeanSeriesTransformer')