from .data_container import MultiDataFrame, MultiSeries
import pandas as pd


class BaseTransformer(object):
    def __init__(self, data_types=None, columns=None, **kwargs):
        raise NotImplemented('Please implement a constructor')

    def fit(self, X, **kwargs):
        raise NotImplemented('Please implement a fit method')

    def transform(self, X):
        raise NotImplemented('Please implement a transform method')

    def fit_transform(self, X):
        obj = self.fit(X)
        transformed_df = obj.transform(X)
        return obj, transformed_df


class CustomTransformer(BaseTransformer):
    def __init__(self, data_types=None, columns=None, **kwargs):
        transform_func = kwargs.get('transform_function')
        if transform_func is None:
            raise ValueError('You mast pass transform_func argument with a function')
        elif not callable(transform_func):
            raise ValueError('transform_func must be callable')

        self.transform_func = transform_func
        self.data_types = data_types
        self.columns = columns

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
                raise ValueError('No column for given data type. Available columns {}'.format(data_types))

    def fit(self, X=None, **kwargs):
        if X is not None:
            self._check_input(X)
        return self

    def _transform_series(self, custom_series):
        return custom_series.apply(self.transform_func)

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

    def transform(self, X):
        self._check_input(X)
        x_type = type(X)

        if x_type == MultiSeries:
            return self._transform_series(X)

        # If X is not MultiSeries, then it's MultiDataFrame
        # Because of self._check_input function
        return self._transform_data_frame(X)


class TimeSeriesTransformer(CustomTransformer):
    def __init__(self, **kwargs):
        accepted_types = [
            pd.Series
        ]

        def series_transform(series):
            return {
                'mean': series.mean(),
                'std': series.std()
            }

        super(TimeSeriesTransformer, self).__init__(data_types=accepted_types,
                                                    columns=None,
                                                    transform_function=series_transform)


class TimeSeriesWindowTransformer(CustomTransformer):
    def __init__(self, **kwargs):
        accepted_types = [
            pd.Series
        ]

        def series_transform(series, **params):
            return series.rolling(window=3).mean()

        super(TimeSeriesWindowTransformer, self).__init__(data_types=accepted_types,
                                                          columns=None,
                                                          transform_function=series_transform)


class PipeLineChain(BaseTransformer):
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
