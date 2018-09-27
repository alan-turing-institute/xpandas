import pandas as pd
import numpy as np
from xpandas.data_container import XSeries, XDataFrame

from xpandas.transformers import XDataFrameTransformer
from xpandas.transformers import PipeLineChain
from xpandas.transformers import XSeriesTransformer
from xpandas.transformers import TimeSeriesWindowTransformer

from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA


n = 1000

xseries = XSeries([
        pd.Series(np.random.normal(size=500))
    ] * n)
my_awesome_transfomer = XSeriesTransformer(transform_function=lambda x: x.std())
my_awesome_transfomer.fit(X)
print(my_awesome_transfomer.transform(X).head())


xdataframe = XDataFrame({
    'gender': XSeries(np.random.binomial(1, 0.7, n)),
    'age': XSeries(np.random.poisson(25, n)),
    'series': xseries
})
df_transformer = XDataFrameTransformer({
    'series': TimeSeriesWindowTransformer(windows_size=4),
    'age': my_awesome_transfomer
})
df_transformer.fit(df)
transformed_df = df_transformer.transform(df)


chain = PipeLineChain([
    ('moving average trans', TimeSeriesWindowTransformer(windows_size=5)),
    ('extract features', my_awesome_transfomer),
    ('pca', PCA(n_components=5)),
    ('logit_regression', LogisticRegression())
])
chain.fit(X)
print(chain.get_params)
transformed_X = chain.transform(X)
