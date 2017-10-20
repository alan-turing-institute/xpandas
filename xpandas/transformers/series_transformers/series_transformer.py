from functools import partial

import pandas as pd
from tsfresh.feature_extraction.extraction import _do_extraction_on_chunk
from tsfresh.feature_extraction.settings import ComprehensiveFCParameters

from ..transformer import XSeriesTransformer


class TimeSeriesTransformer(XSeriesTransformer):
    '''
    Extract common features 'mean', 'std', 'max', 'min',
        'median', 'quantile_25', 'quantile_75',
        'quantile_90', 'quantile_95' from pandas.Series.
    Transform XSeries to XDataFrame.
    '''
    FEATURES = [
        'mean', 'std', 'max', 'min',
        'median', 'quantile_25', 'quantile_75',
        'quantile_90', 'quantile_95'
    ]

    def __init__(self, features=None, **kwargs):
        '''
        :param features: list of features from FEATURES property
        '''
        accepted_types = [
            pd.Series
        ]

        if features is None:
            features = self.FEATURES
        else:
            for f in features:
                if f not in self.FEATURES:
                    raise ValueError('Unrecognized feature {}. Available features {}'.format(f, self.FEATURES))

        def series_transform(series):
            transformed_series = {}

            for f in features:
                if f.startswith('quantile_'):
                    quant_rate = int(f.split('_')[1]) / 100.
                    transformed_series[f] = series.quantile(quant_rate)
                else:
                    method_to_call = getattr(series, f)
                    result = method_to_call()
                    transformed_series[f] = result

            return transformed_series

        super(TimeSeriesTransformer, self).__init__(data_types=accepted_types,
                                                    transform_function=series_transform)


class TimeSeriesWindowTransformer(XSeriesTransformer):
    '''
    Calculate rolling mean over XSeries of pandas.Series.
    '''
    def __init__(self, windows_size=3, **kwargs):
        '''
        :param windows_size: size of window for rolling mean
        '''
        accepted_types = [
            pd.Series
        ]

        self.windows_size = windows_size

        def series_transform(series, **params):
            return series.rolling(window=self.windows_size).mean().dropna()

        super(TimeSeriesWindowTransformer, self).__init__(data_types=accepted_types,
                                                          transform_function=series_transform)


class MeanSeriesTransformer(XSeriesTransformer):
    '''
    Example transformer
    '''
    def __init__(self, **kwargs):
        self.total_mean = None

        def mean_minus_mean_function(s, total_mean=None):
            if total_mean is None:
                total_mean = self.total_mean
            return s.mean() - total_mean

        accepted_types = [
            pd.Series
        ]

        super(MeanSeriesTransformer, self).__init__(data_types=accepted_types,
                                                    transform_function=mean_minus_mean_function)

    def fit(self, X, y=None, **kwargs):
        super(MeanSeriesTransformer, self).fit(X, **kwargs)
        sum_and_size = X.apply(lambda s: (s.sum(), len(s)))
        sum_total = sum([x[0] for x in sum_and_size])
        total_size = sum([x[1] for x in sum_and_size])
        self.total_mean = sum_total / total_size

        return self


class TsFreshSeriesTransformer(XSeriesTransformer):
    '''
    Performs transformation with tsfresh http://tsfresh.readthedocs.io/en/latest/ package
    over XSeries of pandas.Series.
    '''
    def __init__(self, **kwargs):
        accepted_types = [
            pd.Series
        ]

        default_fc_parameters = ComprehensiveFCParameters()
        extraction_function = partial(_do_extraction_on_chunk,
                                      default_fc_parameters=default_fc_parameters,
                                      kind_to_fc_parameters=None)

        def series_transform(series):
            series_name = series.name
            if series_name is None:
                series_name = self.name

            input_series = (
                1, series_name, series
            )
            extracted_data = extraction_function(input_series)
            extracted_data_flat = {
                x['variable']: x['value']
                for x in extracted_data
            }
            return extracted_data_flat

        super(TsFreshSeriesTransformer, self).__init__(data_types=accepted_types,
                                                       columns=None,
                                                       transform_function=series_transform)

    def transform(self, X):
        self.name = X.name
        return super(TsFreshSeriesTransformer, self).transform(X)
