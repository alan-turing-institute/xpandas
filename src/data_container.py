import pandas as pd


def check_all_elements_have_the_same_property(array, func):
    if len(array) == 0:
        return True, None
    try:
        first_element_type = func(array[0])
    except:
        return True, None
    do_all_have_property = all(func(x) == first_element_type
                               for x in array)

    return do_all_have_property, first_element_type


class ObjectWrapper(object):
    def __init__(self, obj):
        self.obj = obj
        self.type = type(obj)


class CustomSeries(pd.Series):
    _metadata = ['data_type']

    @property
    def _constructor(self):
        return CustomSeries

    @property
    def _constructor_expanddim(self):
        return CustomDataFrame

    def __init__(self, *args, **kwargs):
        super(CustomSeries, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        if data is None:
            data = args[0]

        check_result, data_type = check_all_elements_have_the_same_property(data, type)
        if not check_result:
            raise ValueError('Not all elements the same type')

        if data_type is not None:
            self.data_type = data_type
        else:
            self.data_type = type(data._values[0])


class CustomDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return CustomDataFrame

    @property
    def _constructor_sliced(self):
        return CustomSeries

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
            if not isinstance(d, CustomSeries):
                raise ValueError('All data must be CustomSeries instances')
        super(CustomDataFrame, self).__init__(*args, **kwargs)

    def get_columns_of_type(self, column_type):
        columns_to_select = [
            col_name for col_name in self.columns
            if self[col_name].data_type == column_type
        ]

        return self[columns_to_select]
