from src.data_container import MultiDataFrame, MultiSeries
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import tsfresh


class CustomTransformer(BaseEstimator, TransformerMixin):
    _TRANSFORM_ARG_FUNCTION_NAME = 'transform_function'

    def __init__(self, data_types=None, **kwargs):
        transform_function = kwargs.get(self._TRANSFORM_ARG_FUNCTION_NAME)
        if transform_function is not None and not callable(transform_function):
            raise ValueError('transform_function must be callable')

        self.transform_function = transform_function
        self.data_types = data_types

    def _check_input(self, input_data):
        if type(input_data) != MultiDataFrame and type(input_data) != MultiSeries:
            raise ValueError('X must be MultiDataFrame or MultiSeries type')
        elif type(input_data) == MultiSeries and self.data_types is not None \
                and input_data.data_type not in self.data_types:
            raise ValueError('Estimator does not support {} type'.format(input_data.data_type))
        elif type(input_data) == MultiDataFrame:
            data_types = input_data.get_data_types()
            intersection = set(self.data_types) & set(data_types)
            if len(intersection) == 0:
                raise ValueError('No column for given data type. Available columns types {}'.format(data_types))

    def fit(self, X=None, **kwargs):
        if X is not None:
            self._check_input(X)
        return self

    def _transform_series(self, custom_series):
        return custom_series.apply(self.transform_function)

    def _transform_data_frame(self, custom_data_frame):
        sub_df, columns = custom_data_frame.get_columns_of_type(self.data_types)
        transformers_df = custom_data_frame.copy()

        for col in columns:
            transformed_series = self._transform_series(transformers_df[col])
            if type(transformed_series) == MultiSeries:
                transformers_df[col] = transformed_series
            else:
                transformers_df.drop(col, inplace=True, axis=1)
                transformers_df = pd.concat([transformers_df, transformed_series], axis=1)

        return transformers_df

    def transform(self, X, columns=None):
        if not hasattr(self, self._TRANSFORM_ARG_FUNCTION_NAME):
            raise ValueError('You mast pass transform_function argument with a function')

        self._check_input(X)
        x_type = type(X)

        if x_type == MultiSeries:
            return self._transform_series(X)

        # If X is not MultiSeries, then it's MultiDataFrame
        # Because of self._check_input function
        return self._transform_data_frame(X)


class TimeSeriesSimpleTransformer(CustomTransformer):
    def __init__(self, **kwargs):
        accepted_types = [
            pd.Series
        ]

        def series_transform(series):
            return {
                'mean': series.mean(),
                'std': series.std()
            }

        super(TimeSeriesSimpleTransformer, self).__init__(data_types=accepted_types,
                                                    transform_function=series_transform)


class TimeSeriesWindowTransformer(CustomTransformer):
    def __init__(self, windows_size=3, **kwargs):
        accepted_types = [
            pd.Series
        ]

        def series_transform(series, **params):
            return series.rolling(window=windows_size).mean()

        super(TimeSeriesWindowTransformer, self).__init__(data_types=accepted_types,
                                                          transform_function=series_transform)


class MeanSeriesTransformer(CustomTransformer):
    def __init__(self, **kwargs):
        self.total_mean = None
        accepted_types = [
            pd.Series
        ]

        super(MeanSeriesTransformer, self).__init__(data_types=accepted_types)

    def fit(self, X, **kwargs):
        sum_and_size = X.apply(lambda s: (s.sum(), len(s)))
        sum_total = sum([x[0] for x in sum_and_size])
        total_size = sum([x[1] for x in sum_and_size])
        self.total_mean = sum_total / total_size
        return super(MeanSeriesTransformer, self).fit(X, **kwargs)

    def transform(self, X, columns=None):
        f = lambda s: self.total_mean - s.mean()
        self.transform_function = f
        return super(MeanSeriesTransformer, self).transform(X, columns)


class TsFreshSeriesTransformer(CustomTransformer):
    def __init__(self, **kwargs):
        accepted_types = [
            pd.Series
        ]

        def series_transform(series):
            _df = pd.DataFrame({
                'series': series,
                'id': [1 for _ in range(len(series))]
            })
            return tsfresh.extract_features(_df, column_id='id')

        super(TsFreshSeriesTransformer, self).__init__(data_types=accepted_types,
                                                       columns=None,
                                                       transform_function=series_transform)


class PipeLineChain(TransformerMixin):
    def _check_list_of_transforms(self, transforms):
        try:
            is_ok = all(
                len(t) == 2 and type(t[0]) == str
                for t in transforms
            )
        except:
            is_ok = False
        return is_ok

    @property
    def transformers(self):
        return self._transformers

    def __init__(self, *args, **kwargs):
        transforms = kwargs.get('transforms')
        if transforms is None and len(args) == 0:
            raise ValueError('Please pass transforms arguments')
        transforms = args[0]

        if isinstance(transforms, list):
            is_ok = self._check_list_of_transforms(transforms)
        elif isinstance(transforms, dict):
            is_ok = True
        else:
            is_ok = False

        if not is_ok:
            raise TypeError('Wrong value shape of data')

        self._transformers = transforms

    def fit(self, X, **kwargs):
        self.transforms = [
            (t_name, t.fit(X))
            for t_name, t in self._transformers
        ]
        return self

    def transform(self, X):
        transformed_X = X.copy()
        for t_name, t in self._transformers:
            transformed_X = t.transform(transformed_X)

        return transformed_X
