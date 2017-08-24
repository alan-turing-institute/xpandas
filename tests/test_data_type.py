import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from src.data_container import CustomSeries, CustomDataFrame
import pandas as pd
import numpy as np


def test_series_type_series():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    assert s.data_type == pd.Series


def test_series_type_primiteves():
    s1 = CustomSeries([
        1, 2, 3
    ])

    assert s1.data_type == int

    s2 = CustomSeries([
        'a', 'b', 'c'
    ])

    assert s2.data_type == str


def test_series_different_data_type_exception():
    try:
        s1 = CustomSeries([
            pd.Series([1, 2, 3], index=['a', 'b', 'c']),
            pd.DataFrame({})
        ])

        s2 = CustomSeries([
            1, 2, 'abs'
        ])
    except ValueError:
        assert True
        return

    assert False


def test_series_type_data_frame():
    s = CustomSeries([
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
    s = CustomSeries([
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

    s = CustomSeries([
        MyClass(1, 2),
        MyClass(3, 4),
        MyClass(5, 6)
    ])

    assert s.data_type == MyClass

    sub_s = CustomSeries([
        MySubClass(1, 2),
        MySubClass(3, 4),
        MySubClass(5, 6)
    ])

    assert sub_s.data_type == MySubClass


def test_dataframe_data_types():
    s1 = CustomSeries([pd.Series([1, 2, 3], index=['a', 'b', 'c']),
                       pd.Series([4, 5, 6], index=['d', 'e', 'g'])])
    s2 = CustomSeries([1, 2, 3])
    s3 = CustomSeries([{"k1": "v1"}, {"k2": 'v2'}])
    s4 = CustomSeries(['f', 's', 't'])

    df = CustomDataFrame({
        'first_col': s1,
        'second_col': s2,
        'third_col': s3,
        'fourth_col': s4
    })

    assert df['first_col'].data_type == pd.Series
    assert df['second_col'].data_type == np.int64
    assert df['third_col'].data_type == dict
    assert df['fourth_col'].data_type == str

    assert type(df[['first_col']]) == CustomDataFrame
    assert type(df[['first_col', 'second_col']]) == CustomDataFrame