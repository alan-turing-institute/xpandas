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

    def fit(self, X=None, **kwargs):
        if X is not None:
            self._check_input(X)

        return self

    def _transform_series(self, custom_series):
        return custom_series.фзздy(func=self.transform_function)

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
            self.transformations[col_name].fit(X[col_name])

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

                transformers_df = MultiDataFrame.concat_dataframes(
                    [transformers_df, transformed_column]
                )

        return transformers_df
