import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from ..transformers.data_container import MultiSeries, MultiDataFrame
import pandas as pd
import numpy as np


def test_series_type_series():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    assert s.data_type == pd.Series


def test_series_type_primiteves():
    s1 = MultiSeries([
        1, 2, 3
    ])

    assert s1.data_type == np.int64

    s2 = MultiSeries([
        'a', 'b', 'c'
    ])

    assert s2.data_type == str


def test_series_different_data_type_exception():
    try:
        s1 = MultiSeries([
            pd.Series([1, 2, 3], index=['a', 'b', 'c']),
            pd.DataFrame({})
        ])

        s2 = MultiSeries([
            1, 2, 'abs'
        ])
    except ValueError:
        assert True
        return

    assert False


def test_series_type_data_frame():
    s = MultiSeries([
        pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        }),
        pd.DataFrame({
            'c': [7, 8, 9],
            'd': [10, 11, 12]
        })
    ])

    assert s.data_type == pd.DataFrame


def test_series_slise_type():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g']),
        pd.Series([7, 8, 9])
    ])

    sub_s = s[:2]

    assert sub_s.data_type == pd.Series


def test_series_custom_class_type():
    class MyClass(object):
        a = 1
        b = 2

        def __init__(self, a, b):
            self.a = a
            self.b = b

    class MySubClass(MyClass):
        pass

    s = MultiSeries([
        MyClass(1, 2),
        MyClass(3, 4),
        MyClass(5, 6)
    ])

    assert s.data_type == MyClass

    sub_s = MultiSeries([
        MySubClass(1, 2),
        MySubClass(3, 4),
        MySubClass(5, 6)
    ])

    assert sub_s.data_type == MySubClass


def test_dataframe_data_types():
    s1 = MultiSeries([pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                      pd.Series([4, 5, 6], index=['d', 'e', 'g'])])
    s2 = MultiSeries([1, 2, 3])
    s3 = MultiSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = MultiSeries(['f', 's', 't'])

    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    assert df['first_col'].data_type == pd.Series
    assert df['second_col'].data_type == np.int64
    assert df['third_col'].data_type == dict
    assert df['fourth_col'].data_type == str

    assert type(df[['first_col']]) == MultiDataFrame
    assert type(df[['first_col', 'second_col']]) == MultiDataFrame


def test_dataframe_sub_frame_data_types():
    s1 = MultiSeries([pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                      pd.Series([4, 5, 6], index=['d', 'e', 'g'])])
    s2 = MultiSeries([1, 2, 3])
    s3 = MultiSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = MultiSeries(['f', 's', 't'])

    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    sub_df = df.loc[:2]

    assert type(sub_df) == MultiDataFrame
    assert sub_df['first_col'].data_type == pd.Series
    assert sub_df['second_col'].data_type == np.int64
    assert sub_df['third_col'].data_type == dict
    assert sub_df['fourth_col'].data_type == str

    assert type(sub_df[['first_col']]) == MultiDataFrame
    assert type(sub_df[['first_col', 'second_col']]) == MultiDataFrame


def test_series_map_transformer():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    func = lambda series: series + 1
    mapped_s = s.map(func)
    assert mapped_s.data_type == pd.Series
    assert mapped_s[0].equals(pd.Series([2, 3, 4], index=['a', 'b', 'c']))

    func = lambda series: series.mean()
    mapped_s = s.map(func)
    assert mapped_s.data_type == np.float64


def test_series_extract_features_with_apply_func():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ], name='MySuperSeries')

    func = lambda series: {'mean': series.mean(), 'std': series.std()}
    mapped_s = s.apply(func)
    assert type(mapped_s) == MultiDataFrame


def test_series_replace_element():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ], name='MySuperSeries')

    try:
        s[0] = 111
        assert False
    except:
        assert True

    try:
        s[0] = pd.Series(np.random.normal(size=100))
        assert True
    except:
        assert False


def test_series_to_pandas_series():
    s = MultiSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ], name='MySuperSeries')
    s = MultiSeries(['a', 'b', 'c'], name='MySuperSeries')
    s = s.to_pandas_series()

    assert type(s) == pd.Series


def test_dataframe_to_pandas_dataframe():
    s1 = MultiSeries([pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                      pd.Series([4, 5, 6], index=['d', 'e', 'g'])])
    s2 = MultiSeries([1, 2, 3])
    s3 = MultiSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = MultiSeries(['f', 's', 't'])

    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    try:
        df.to_pandas_dataframe()
        assert False
    except:
        assert True

    s1 = MultiSeries([4, 5, 6])
    s2 = MultiSeries([1, 2, 3])

    df = MultiDataFrame({
        'first_col': s1,
        'second_col': s2,
    })

    try:
        df = df.to_pandas_dataframe()
        assert True
    except:
        assert False

    assert type(df) == pd.DataFrame