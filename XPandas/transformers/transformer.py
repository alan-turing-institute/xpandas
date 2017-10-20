from sklearn.base import BaseEstimator, TransformerMixin

from ..data_container import XDataFrame, XSeries


class XSeriesTransformer(BaseEstimator, TransformerMixin):
    '''
    XSeriesTransformer is a base class for all custom transformers.
    XSeriesTransformer is a high level abstraction to transform XSeries of
    specific data_types to an another XSeries or XDataFrame.
    XSeriesTransformer encapsulates transformation and based on scikit-learn BaseEstimator
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
        Check that input valid: input_data is XSeries and transformer
        "knows" how to work with input_data.data_type.
        In error raise exception.
        '''
        if type(input_data) != XSeries:
            raise ValueError('X must be XSeries type')
        elif type(input_data) == XSeries and self.data_types is not None \
                and input_data.data_type not in self.data_types:
            raise ValueError('Estimator does not support {} type'.format(input_data.data_type))

    def fit(self, X=None, y=None, **kwargs):
        '''
        Fit transformer for giver data.
        Must be overwritten in child classes
        :param X: XSeries to fit transformer on
        :param y: Labels column for X
        :param kwargs: additional arguments for transformer
        :return: fitted self object
        '''
        if X is not None:
            self._check_input(X)

        return self

    def _transform_series(self, custom_series):
        '''
        Helper method to transform XSeries
        :param custom_series: XSeries object
        :return: transformed XSeries.
                 it could be XSeries or XDataFrame object
        '''
        return custom_series.apply(func=self.transform_function, prefix=self.name)

    def transform(self, X):
        '''
        Apply transformation to X with current transformer
        :param X: input XSeries
        :param columns: deprecated
        :return: transformed XSeries.
                 it could be XSeries or XDataFrame object

        '''
        if not hasattr(self, self._TRANSFORM_ARG_FUNCTION_NAME):
            raise ValueError('You mast pass transform_function argument with a function')

        self._check_input(X)

        transform_series = self._transform_series(X)
        transform_series.index = X.index

        return transform_series


class XDataFrameTransformer(BaseEstimator, TransformerMixin):
    '''
    XDataFrameTransformer is a set of XSeriesTransformer instances.
    XDataFrameTransformer can transform XDataFrame object to another XDataFrame
    based on set of XSeriesTransformer transformers.
    '''

    def _validate_transformations(self, transformations):
        for k, v in transformations.items():
            if not isinstance(k, str):
                raise TypeError('Key must be a string {}'.format(k))

            if isinstance(v, list):
                for t in v:
                    if not isinstance(t, XSeriesTransformer):
                        raise TypeError('All objects of {} must be a Transformer object. Issue with {}'.format(v, t))
            elif not isinstance(v, XSeriesTransformer):
                raise TypeError('Value must be a Transformer object {}'.format(v))

    def _wrap_transformers_in_list(self, transformations):
        new_transformers = {}
        for k, v in transformations.items():
            if isinstance(v, list):
                new_transformers[k] = v
            else:
                new_transformers[k] = [v]
        return new_transformers

    def __init__(self, transformations):
        '''
        Init XDataFrameTransformer with a dict of transformations.
        Each transformation specify column and transformer object
        :param transformations: dict {column_name: Transformer object or [Transformer object]}
        '''
        self._validate_transformations(transformations)
        self.transformations = self._wrap_transformers_in_list(transformations)

    def fit(self, X=None, y=None, **kwargs):
        '''
        Fit each transformer at self.transformations dictionary
        '''
        if not isinstance(X, XDataFrame):
            raise TypeError('X must be a XDataFrame type. Not {}'.format(type(X)))

        for col_name, transformations in self.transformations.items():
            for t in transformations:
                t.fit(X[col_name])

        return self

    def transform(self, X, columns_mapping=None):
        '''
        Transform X with fitted dictionary self.transformations.
        :param columns_mapping: {old_col: new_col} mapping between columns in fit data set and current X
        :return:
        '''
        if columns_mapping is None:
            columns_mapping = {}

        transformers_df = X.copy()

        for col_name, transformations in self.transformations.items():
            for t in transformations:
                new_col_name = columns_mapping.get(col_name, col_name)
                transformed_column = t.transform(X[new_col_name])

                if type(transformed_column) == XSeries:
                    transformers_df.rename(columns={
                        new_col_name: transformed_column.name
                    }, inplace=True)
                    transformers_df[transformed_column.name] = transformed_column
                else:
                    transformers_df.drop(new_col_name, inplace=True, axis=1)

                    transformers_df = XDataFrame.concat_dataframes(
                        [transformers_df, transformed_column]
                    )

        return transformers_df
