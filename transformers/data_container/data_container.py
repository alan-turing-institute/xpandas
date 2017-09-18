import numpy as np
import pandas as pd


def check_all_elements_have_the_same_property(array, func):
    if len(array) == 0:
        return True, None
    try:
        first_element_type = func(array[0])
    except:
        return True, None
    #
    # if len(array) == 3:
    #     print('\n\n\n')
    #     print(array)
    #     array = array[~np.isnan(array)]
    #     array = [
    #         x for x in array
    #         if not np.isnan(x)
    #     ]
    #
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


class MultiSeries(pd.Series):
    _metadata = ['data_type']

    @property
    def _constructor(self):
        return MultiSeries

    @property
    def _constructor_expanddim(self):
        return MultiDataFrame

    def __init__(self, *args, **kwargs):
        super(MultiSeries, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        if data is None:
            data = args[0]

        check_result, data_type = check_all_elements_have_the_same_property(data, type)
        if not check_result:
            raise ValueError('Not all elements the same type')

        if data_type is not None:
            self._data_type = data_type
        else:
            self._data_type = type(data._values[0])

    def apply(self, *args, **kwargs):
        func = kwargs.get('func')
        if func is None:
            func = args[0]

        # nan_index = self.isnull()

        # TODO
        # Possibly change!!! to handle NaN also
        mapped_series = self.dropna()
        mapped_series = mapped_series.map(func, na_action='ignore')
        # print(mapped_series.shape)
        mapped_data_type = mapped_series.data_type

        custom_prefix = kwargs.get('prefix')
        if custom_prefix is None:
            custom_prefix = self.name

        if mapped_data_type == dict:
            custom_df = MultiDataFrame.from_records(mapped_series.values)

            if custom_prefix is not None:
                custom_df.columns = custom_df.columns.map(lambda x: '{}_{}'.format(custom_prefix, x))
            return custom_df
        elif mapped_data_type == pd.DataFrame:
            return pd.concat(mapped_series.values, ignore_index=True)

        return mapped_series

    @property
    def data_type(self):
        first_element_data_type = type(self.iloc[0])
        self._data_type = first_element_data_type
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        self._data_type = data_type

    def to_pandas_series(self):
        is_primitive = _is_class_a_primitive(self.data_type)
        if is_primitive:
            self.__class__ = pd.Series
        else:
            raise ValueError('Unable to cast to pd.Series. {} is not a primitive type.'.format(self.data_type))
        return self

    def __str__(self):
        s = super(MultiSeries, self).__str__()
        return '{}\ndata_type: {}'.format(s, self.data_type)

    def __getitem__(self, key):
        return super(MultiSeries, self).__getitem__(key)

    def __setitem__(self, key, value):
        value_type = type(value)
        if value_type != self.data_type:
            raise ValueError('Can not assign key {} with {} wrong data_type {} correct is {}'.format(
                key, value, value_type, self.data_type
            ))

        return super(MultiSeries, self).__setitem__(key, value)


class MultiDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return MultiDataFrame

    @property
    def _constructor_sliced(self):
        return MultiSeries

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is None:
            data = args[0]

        data_to_check = []
        if isinstance(data, list):
            data_to_check = data
        elif isinstance(data, dict):
            data_to_check = data.values()

        for d in data_to_check:
            if not isinstance(d, MultiSeries):
                raise ValueError('All data must be MultiSeries instances')
        super(MultiDataFrame, self).__init__(*args, **kwargs)

    def get_columns_of_type(self, column_type):
        '''
        :param column_type: list of types
        :return: Return columns from MultiDataFrame (list of names)
                + sub MultiDataFrame
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
        data_types = [
            self[column].data_type
            for column in self
        ]
        return data_types

    def to_pandas_dataframe(self):
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
        return pd.concat(data_frames, axis=1)
