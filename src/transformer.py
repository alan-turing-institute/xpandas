import pandas as pd

class BaseTransformer(object):
    def __init__(self, **params):
        raise NotImplemented()

    def fit(self, X, y=None):
        raise NotImplemented()

    def transform(self, X):
        raise NotImplemented()


class TimeSeriesTransformer(BaseTransformer):
    def __init__(self, **params):
        self.accepted_fields = [
            pd.Series
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        pass


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

    def __init__(self, **params):
        super(PipeLineChain, self).__init__(**params)
        transforms = params.get('transforms')
        if transforms is None:
            raise ValueError('Please pass transforms arguments')

        if isinstance(transforms, list):
            is_ok = self._check_list_of_transforms(transforms)
        elif isinstance(transforms, dict):
            is_ok = True
        else:
            is_ok = False

        if not is_ok:
            raise TypeError('Wrong value shape of data')

        self.transforms = transforms
