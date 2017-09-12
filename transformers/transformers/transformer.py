from ..data_container import MultiDataFrame, MultiSeries
from sklearn.base import BaseEstimator, TransformerMixin


class CustomTransformer(BaseEstimator, TransformerMixin):
    _TRANSFORM_ARG_FUNCTION_NAME = 'transform_function'

    def __init__(self, data_types=None, **kwargs):
        transform_function = kwargs.get(self._TRANSFORM_ARG_FUNCTION_NAME)
        if transform_function is not None and not callable(transform_function):
            raise ValueError('transform_function must be callable')

        self.transform_function = transform_function
        self.data_types = data_types

    def _check_input(self, input_data):
        if type(input_data) != MultiSeries:
            raise ValueError('X must be MultiSeries type')
        elif type(input_data) == MultiSeries and self.data_types is not None \
                and input_data.data_type not in self.data_types:
            raise ValueError('Estimator does not support {} type'.format(input_data.data_type))

            # if type(input_data) != MultiDataFrame and type(input_data) != MultiSeries:
            #     raise ValueError('X must be MultiDataFrame or MultiSeries type')
            # elif type(input_data) == MultiSeries and self.data_types is not None \
            #         and input_data.data_type not in self.data_types:
            #     raise ValueError('Estimator does not support {} type'.format(input_data.data_type))
            # elif type(input_data) == MultiDataFrame:
            #     data_types = input_data.get_data_types()
            #     intersection = set(self.data_types) & set(data_types)
            #     if len(intersection) == 0:
            #         raise ValueError('No column for given data type. Available columns types {}'.format(data_types))

    def fit(self, X=None, **kwargs):
        if X is not None:
            self._check_input(X)

        return self

    def _transform_series(self, custom_series):
        return custom_series.apply(func=self.transform_function)

    '''
    def _transform_data_frame(self, custom_data_frame, custom_columns=None):
        sub_df, columns = custom_data_frame.get_columns_of_type(self.data_types)
        if custom_columns is not None:
            columns = [
                col for col in columns
                if col in custom_columns
            ]

        transformers_df = custom_data_frame.copy()

        for col in columns:
            transformed_series = self._transform_series(transformers_df[col])
            if type(transformed_series) == MultiSeries:
                transformers_df[col] = transformed_series
            else:
                transformers_df.drop(col, inplace=True, axis=1)
                transformers_df = pd.concat([transformers_df, transformed_series], axis=1)

        return transformers_df
    '''

    def transform(self, X, columns=None):
        if not hasattr(self, self._TRANSFORM_ARG_FUNCTION_NAME):
            raise ValueError('You mast pass transform_function argument with a function')

        self._check_input(X)

        return self._transform_series(X)


class DataFrameTransformer(BaseEstimator, TransformerMixin):
    def _validate_transformations(self, transformations):
        for k, v in transformations.items():
            if not isinstance(k, str):
                raise TypeError('Key must be a string {}'.format(k))
            if not isinstance(v, CustomTransformer):
                raise TypeError('Value must be a Transformer object {}'.format(v))

    def __init__(self, transformations):
        '''
        :param transformations: dict {column_name: Transformer object}
        '''
        self._validate_transformations(transformations)
        self.transformations = transformations

    def fit(self, X=None, **kwargs):
        if not isinstance(X, MultiDataFrame):
            raise TypeError('X must be a MultiDataFrame type. Not {}'.format(type(X)))

        for col_name in self.transformations.keys():
            self.transformations = self.transformations[col_name].fit(X[col_name])

        return self

    def transform(self, X, columns_mapping=None):
        '''
        :param columns_mapping: {old_col: new_col} mapping
        :return:
        '''
        if columns_mapping is None:
            columns_mapping = {}

        transformers_df = X.copy()

        for col_name, transformer in self.transformations.items():
            new_col_name = columns_mapping.get(col_name, col_name)
            transformed_column = transformer.transform(X[new_col_name])

            if type(transformed_column) == MultiSeries:
                transformers_df[new_col_name] = transformed_column
            else:
                transformers_df.drop(new_col_name, inplace=True, axis=1)
                transformers_df = MultiDataFrame([transformers_df, transformed_column])

        return transformers_df