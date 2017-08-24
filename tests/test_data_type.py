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



