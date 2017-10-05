from collections import Counter

import numpy as np
import pandas as pd

from ..transformer import XSeriesTransformer


class BagOfWordsTransformer(XSeriesTransformer):
    '''
    Performs bag-of-features transformer for strings of any categorical data.
    '''
    def __init__(self, dictionary=None, **kwargs):
        '''
        :param dictionary: custom dictionary to count against. if None, calculate dictionary from dataset
        '''
        self.dictionary = dictionary

        accepted_types = [
            pd.Series, list, np.array, tuple
        ]

        def bag_of_words_transform_function(corpus):
            counter = Counter(corpus)
            for el in self.dictionary:
                if counter.get(el) is None:
                    counter[el] = 0
            return counter

        super(BagOfWordsTransformer, self).__init__(data_types=accepted_types,
                                                    columns=None,
                                                    transform_function=bag_of_words_transform_function)

    def __calculate_dictionary(self, X):
        dictionary = set()
        for el in X:
            dictionary = dictionary.union(el)
        return dictionary

    def fit(self, X=None, y=None, **kwargs):
        super(BagOfWordsTransformer, self).fit(X, y, **kwargs)
        if self.dictionary is not None:
            return self
        self.dictionary = self.__calculate_dictionary(X)
        return self
