import numpy as np
import pandas as pd


def _check_all_elements_have_the_same_property(array, func):
    '''
    Helper function that checks if all elements have the same func(element) value.
    :param array: input values
    :param func: any callable object
    :return: tuple. the first element indicates is all elements are have the same func(element) value,
             second element is a value of func(element)
    '''
    if len(array) == 0:
        return True, None
    try:
        first_element_type = func(array[0])
    except:
        return True, None
    do_all_have_property = all(func(x) == first_element_type
                               for x in array)

    return do_all_have_property, first_element_type


def _is_class_a_primitive(cls):
    '''
    Check if class is a number or string including numpy numbers
    :param cls: any class
    :return: True if class is a primitive class, else False
    '''
    primitives = [
        np.float16, np.float32, np.float64, np.float128,
        np.int8, np.int16, np.int32, np.int64,
        bool, str, np.uint8, np.uint16, np.uint32, np.uint64,
        int, float
    ]
    return cls in primitives


class XSeries(pd.Series):
    '''
    XSeries is an homogeneous abstract 1d container that encapsulates any data type inside.
    It is an extension of pandas.Series class.
    XSeries has a property data_type that is a type ot objects that are inside XSeries.
    '''
    _metadata = ['data_type']

    @property
    def _constructor(self):
        return XSeries

    @property
    def _constructor_expanddim(self):
        return XDataFrame

    def __init__(self, *args, **kwargs):
        '''
        The same arguments as for pandas.Series
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html

        In order to create XSeries of any data_type, data argument must be a pythons list.
        For example, to create XSeries of pandas.Series, pass data should be
        data = [s_1, s2, ..., s3] where s_i is a instance of pandas.Series.
        '''
        super(XSeries, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        if data is None:
            data = args[0]

        check_result, data_type = _check_all_elements_have_the_same_property(data, type)
        if not check_result:
            raise ValueError('Not all elements the same type')

        if data_type is not None:
            self._data_type = data_type
        else:
            self._data_type = type(data._values[0])

    def apply(self, *args, **kwargs):
        '''
        Overwrite standart pandas.Series method.
        Apply transform function to all elements in self.
        *If transform function return dict like object,
        transform XSeries to XDataFrame see XDataFrame constructor*

        :param func: function to apply
        :param prefix: prefix for columns if needs to return XDataFrame object
        :return: XSeries of XDataFrame depending on transformation
        '''
        func = kwargs.get('func')
        if func is None:
            func = args[0]

        # TODO
        # Possibly change to handle NaN
        mapped_series = self.dropna()
        mapped_series = mapped_series.map(func, na_action='ignore')
        mapped_data_type = mapped_series.data_type

        custom_prefix = kwargs.get('prefix')
        if custom_prefix is None:
            custom_prefix = self.name
        else:
            custom_prefix = '{}_{}'.format(self.name, custom_prefix)

        if mapped_series.__is_data_type_dict_like():
            custom_df = XDataFrame.from_records(mapped_series.values)

            if custom_prefix is not None:
                custom_df.columns = custom_df.columns.map(lambda x: '{}_{}'.format(custom_prefix, x))
            return custom_df
        elif mapped_data_type == pd.DataFrame:
            return pd.concat(mapped_series.values, ignore_index=True)
        else:
            mapped_series.name = custom_prefix

        return mapped_series

    def __is_data_type_dict_like(self):
        '''
        Check if data encapsulated by self is instance of dict
        '''
        return isinstance(self.iloc[0], dict)

    @property
    def data_type(self):
        '''
        Getter for a data_type property
        data_type is a data type that self encapsulates
        For example, if self is contains images, that data_type would be Image
        '''
        first_element_data_type = type(self.iloc[0])
        self._data_type = first_element_data_type
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        '''
        Setter for a data_type property
        data_type is a data type that self encapsulates
        For example, if self is contains images, that data_type would be Image
        '''

        self._data_type = data_type

    def to_pandas_series(self):
        '''
        Convert self to pandas.Series if data_type is a primitive type
        etc. number of string
        :return: Pandas Series or raise exception if data_type is not a primitive type
        '''
        is_primitive = _is_class_a_primitive(self.data_type)
        if is_primitive:
            self.__class__ = pd.Series
        else:
            raise ValueError('Unable to cast to pd.Series. {} is not a primitive type.'.format(self.data_type))
        return self

    def __str__(self):
        s = super(XSeries, self).__str__()
        return '{}\ndata_type: {}'.format(s, self.data_type)

    def __getitem__(self, key):
        return super(XSeries, self).__getitem__(key)

    def __setitem__(self, key, value):
        value_type = type(value)
        if value_type != self.data_type:
            raise ValueError('Can not assign key {} with {} wrong data_type {} correct is {}'.format(
                key, value, value_type, self.data_type
            ))

        return super(XSeries, self).__setitem__(key, value)


class XDataFrame(pd.DataFrame):
    '''
    XDataFrame is 2d container that stores XSeries objects
    XDataFrame is an extension of pandas.DataFrame object
    '''

    @property
    def _constructor(self):
        return XDataFrame

    @property
    def _constructor_sliced(self):
        return XSeries

    def __init__(self, *args, **kwargs):
        '''
        The same arguments as for pandas.DataFrame
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html

        data argument should be a list of XSeries objects or dict of XSeries objects.
        In dict is passed, key must be a string and it's indicate appropriate column name.
        For example, to create XDataFrame data should looks like
        data = {'col_1': s_1, 'col_2': s_2, ..., 'col_n': s_n} where s_i is a XSeries
        '''
        data = kwargs.get('data')
        if data is None:
            data = args[0]

        data_to_check = []
        if isinstance(data, list):
            data_to_check = data
        elif isinstance(data, dict):
            data_to_check = data.values()

        for d in data_to_check:
            if not isinstance(d, XSeries):
                raise ValueError('All data must be XSeries instances')
        super(XDataFrame, self).__init__(*args, **kwargs)

    def get_columns_of_type(self, column_type):
        '''
        Get all columns from XDataFrame with given column_type
        :param column_type: list of types or a single type
        :return: tuple. the first element is subMultiDataFrame and second is a list of column of a given column_type
        '''
        if type(column_type) != list:
            column_type = [column_type]

        columns_to_select = [
            col_name
            for col_name in self
            if self[col_name].data_type in column_type
        ]

        return self[columns_to_select], columns_to_select

    def get_data_types(self):
        '''
        Get a list of data_types of each XSeries inside XDataFrame
        :return: list of data_type
        '''
        data_types = [
            self[column].data_type
            for column in self
        ]
        return data_types

    def to_pandas_dataframe(self):
        '''
        Convert self to pandas.DataFrame if all columns are primitive types.
        See more at XSeries.to_pandas_series
        :return:
        '''
        data_types = self.get_data_types()
        is_all_columns_are_primitive = all(
            _is_class_a_primitive(dt)
            for dt in data_types
        )
        if is_all_columns_are_primitive:
            self.__class__ = pd.DataFrame
        else:
            raise ValueError('Unable to cast to pd.DataFrame. {} is not all primitives.'.format(self.data_types))
        return self

    @classmethod
    def concat_dataframes(cls, data_frames):
        '''
        Concatenate XDataFrame using pandas.concat method
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.concat.html
        over columns
        :param data_frames: list of XDataFrame instances
        :return: XDataFrame — concatenated list of data_frames
        '''
        return pd.concat(data_frames, axis=1)
