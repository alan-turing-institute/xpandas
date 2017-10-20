import string

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import PCA

from ..xpandas.data_container import XSeries, XDataFrame
from ..xpandas.transformers import XSeriesTransformer
from ..xpandas.transformers.bag_of_features_transformer import BagOfWordsTransformer
from ..xpandas.transformers.pipeline_transformer import PipeLineChain


def test_bag_of_words_for_series():
    dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                                 remove=('headers', 'footers', 'quotes'))

    series = XSeries(dataset.data[:10])
    assert series.data_type == str

    translator = str.maketrans('', '', string.punctuation)
    tokenizer_transformer = XSeriesTransformer(
        transform_function=lambda text: text.lower().translate(translator).strip().split()
    )

    transformed_series = tokenizer_transformer.fit_transform(series)
    # print(transformed_series)

    bag_transform = BagOfWordsTransformer()

    transformed_series = bag_transform.fit_transform(transformed_series)

    # print(transformed_series)

    assert type(transformed_series) == XDataFrame


def test_bag_of_words_for_series_pipeline():
    dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                                 remove=('headers', 'footers', 'quotes'))
    n = 100
    series = XSeries(dataset.data[:n])
    assert series.data_type == str

    translator = str.maketrans('', '', string.punctuation)
    tokenizer_transformer = XSeriesTransformer(
        transform_function=lambda text: text.lower().translate(translator).strip().split()
    )

    # series = tokenizer_transformer.transform(series)

    Y = np.random.binomial(1, 0.5, n)

    pipeline = PipeLineChain([
        ('preprocessing', XSeriesTransformer(
            transform_function=lambda text: text.lower().translate(translator).strip().split()
        )),
        ('extractor', BagOfWordsTransformer()),
        ('pca', PCA(n_components=10)),
        # ('svc', LinearSVC())
    ])

    pipeline = pipeline.fit(series)
    transformed_series = pipeline.transform(series)

    # print(transformed_series)
