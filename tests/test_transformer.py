import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, ".."))

from src.data_container import CustomSeries, CustomDataFrame
from src.transformer import CustomTransformer
import pandas as pd
import numpy as np


def test_transformer():
    s = CustomSeries([
        pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        pd.Series([4, 5, 6], index=['d', 'e', 'g'])
    ])

    func = lambda series: series + 1

    mapped_s = s.map(func)

    print(mapped_s)
    print(mapped_s.data_type)

    # print('Type {}'.format(s.data_type))
    # assert type(mapped_s) == CustomSeries

    # print(type(mapped_s[0]))
    # print(mapped_s.data_type)
