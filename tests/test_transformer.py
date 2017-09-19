import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from ..transformers.data_container import MultiDataFrame, MultiSeries
from ..transformers.transformers import CustomTransformer, TimeSeriesTransformer,\
    TimeSeriesWindowTransformer, MeanSeriesTransformer, DataFrameTransformer, PipeLineChain
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

    series_to_series_transformer = TimeSeriesWindowTransformer(windows_size=5)
    series_to_series_transformer.set_params(windows_size=3)
    series_to_series_transformer.fit()
    transformed_series = series_to_series_transformer.transform(s)

    assert series_to_series_transformer.transform_function(s[0]).equals(transformed_series[0])
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
    s4 = MultiSeries(['f', 's'])
    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    # print(
    #     df['first_col'].shape
    # )

    data_frame_transformer = DataFrameTransformer(transformations={
        'first_col': TimeSeriesTransformer(),
        'second_col': TimeSeriesTransformer()
    })

    data_frame_transformer.fit(df)
    transformers_df = data_frame_transformer.transform(df)
    # print(transformers_df.head())


def test_pipeline_transformer_for_series():
    from sklearn.decomposition import PCA

    s1 = MultiSeries([
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=15))
    ])

    pipeline = PipeLineChain(
        [
            ('first_transformer', TimeSeriesWindowTransformer()),
            ('mean_transformer', TimeSeriesTransformer())
        ]
    )
    pipeline = pipeline.fit(s1)
    transformed_ts = pipeline.transform(s1)

    pipeline = PipeLineChain(
        [
            ('first_transformer', TimeSeriesWindowTransformer()),
            ('mean_transformer', TimeSeriesTransformer()),
            ('pca', PCA(n_components=4))
        ]
    )
    pipeline.fit(s1)
    transformed_ts = pipeline.transform(s1)


def test_mean_transformer():
    s1 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=15))
    ])
    s2 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=15)),
        pd.Series(np.random.normal(size=100))
    ])

    tr = MeanSeriesTransformer()
    tr = tr.fit(s1)

    transformed_s = tr.transform(s2)

    assert transformed_s.shape[0] == 3
    assert type(transformed_s) == MultiSeries


def test_mean_transformer_data_frame():
    s1 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=15))
    ])
    s2 = MultiSeries([
        pd.Series(np.random.normal(size=10)),
        pd.Series(np.random.normal(size=15))
    ])

    df = MultiDataFrame({
        's1': s1,
        's2': s2
    })

    tr = MeanSeriesTransformer()
    try:
        tr = tr.fit(df)
        assert False
    except:
        assert True
