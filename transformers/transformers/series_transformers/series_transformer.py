from ..transformer import CustomTransformer
import pandas as pd
import tsfresh


class TimeSeriesTransformer(CustomTransformer):
    FEATURES = [
        'mean', 'std', 'max', 'min',
        'median', 'quantile_25', 'quantile_75',
        'quantile_90', 'quantile_95'
    ]

    def __init__(self, features=None, **kwargs):
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

        def mean_minus_mean_function(s, total_mean=None):
            if total_mean is None:
                total_mean = self.total_mean
            return s.mean() - total_mean

        accepted_types = [
            pd.Series
        ]

        super(MeanSeriesTransformer, self).__init__(data_types=accepted_types,
                                                    transform_function=mean_minus_mean_function)

    def fit(self, X, **kwargs):
        super(MeanSeriesTransformer, self).fit(X, **kwargs)
        sum_and_size = X.apply(lambda s: (s.sum(), len(s)))
        sum_total = sum([x[0] for x in sum_and_size])
        total_size = sum([x[1] for x in sum_and_size])
        self.total_mean = sum_total / total_size

        return self


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
