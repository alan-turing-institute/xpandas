from main import CustomSeries, CustomDataFrame
import numpy as np
import pandas as pd


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

# df = CustomDataFrame([
#        s1, s2, s3, s4
# ])
# s = df['third']

print(
    df.fourth_col.data_type
)