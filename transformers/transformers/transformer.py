from sklearn.base import BaseEstimator, TransformerMixin

from ..data_container import MultiDataFrame, MultiSeries


class CustomTransformer(BaseEstimator, TransformerMixin):
    '''
    CustomTransformer is a base class for all custom transformers.
    CustomTransformer is a high level abstraction to transform MultiSeries of
    specific data_types to an another MultiSeries or MultiDataFrame.
    CustomTransformer encapsulates transformation and based on scikit-learn BaseEstimator
    http://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html
    '''
    _TRANSFORM_ARG_FUNCTION_NAME = 'transform_function'

    def __init__(self, transform_function=None, data_types=None, name=None, **kwargs):
        '''
        :param transform_function: Callable that performs actual transform
        :param data_types: list of data_type that this transformer can work with. if None,
                            error might be raised at run time
        :param name: name for transformer. if none, class name is default
        :param kwargs: additional arguments
        '''
        if transform_function is not None and not callable(transform_function):
            raise ValueError('transform_function must be callable')

        self.transform_function = transform_function
        self.data_types = data_types

        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def _check_input(self, input_data):
        '''
        Check that input valid: input_data is MultiSeries and transformer
        "knows" how to work with input_data.data_type.
        In error raise exception.
        '''
        if type(input_data) != MultiSeries:
            raise ValueError('X must be MultiSeries type')
        elif type(input_data) == MultiSeries and self.data_types is not None \
                and input_data.data_type not in self.data_types:
            raise ValueError('Estimator does not support {} type'.format(input_data.data_type))

    def fit(self, X=None, y=None, **kwargs):
        '''
        Fit transformer for giver data.
        Must be overwritten in child classes
        :param X: MultiSeries to fit transformer on
        :param y: Labels column for X
        :param kwargs: additional arguments for transformer
        :return: fitted self object
        '''
        if X is not None:
            self._check_input(X)

        return self

    def _transform_series(self, custom_series):
        '''
        Helper method to transform MultiSeries
        :param custom_series: MultiSeries object
        :return: transformed MultiSeries.
                 it could be MultiSeries or MultiDataFrame object
        '''
        return custom_series.apply(func=self.transform_function, prefix=self.name)

    def transform(self, X):
        '''
        Apply transformation to X with current transformer
        :param X: input MultiSeries
        :param columns: deprecated
        :return: transformed MultiSeries.
                 it could be MultiSeries or MultiDataFrame object

        '''
        if not hasattr(self, self._TRANSFORM_ARG_FUNCTION_NAME):
            raise ValueError('You mast pass transform_function argument with a function')

        self._check_input(X)

        transform_series = self._transform_series(X)
        transform_series.index = X.index

        return transform_series


class DataFrameTransformer(BaseEstimator, TransformerMixin):
    '''
    DataFrameTransformer is a set of CustomTransformer instances.
    DataFrameTransformer can transform MultiDataFrame object to another MultiDataFrame
    based on set of CustomTransformer transformers.
    '''
    def _validate_transformations(self, transformations):
        for k, v in transformations.items():
            if not isinstance(k, str):
                raise TypeError('Key must be a string {}'.format(k))
            if not isinstance(v, CustomTransformer):
                raise TypeError('Value must be a Transformer object {}'.format(v))

    def __init__(self, transformations):
        '''
        Init DataFrameTransformer with a dict of transformations.
        Each transformation specify column and transformer object
        :param transformations: dict {column_name: Transformer object}
        '''
        self._validate_transformations(transformations)
        self.transformations = transformations

    def fit(self, X=None, y=None, **kwargs):
        '''
        Fit each transformer at self.transformations dictionary
        '''
        if not isinstance(X, MultiDataFrame):
            raise TypeError('X must be a MultiDataFrame type. Not {}'.format(type(X)))

        for col_name in self.transformations.keys():
            self.transformations[col_name].fit(X[col_name])

        return self

    def transform(self, X, columns_mapping=None):
        '''
        Transform X with fitted dictionary self.transformations.
        :param columns_mapping: {old_col: new_col} mapping between columns in fit dataset and current X
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
