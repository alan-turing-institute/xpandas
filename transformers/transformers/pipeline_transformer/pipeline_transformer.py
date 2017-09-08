from sklearn.base import BaseEstimator, TransformerMixin


class PipeLineChain(TransformerMixin):
    def _check_list_of_transforms(self, transforms):
        try:
            is_ok = all(
                len(t) > 1 and type(t[0]) == str
                for t in transforms
            )
        except:
            is_ok = False
        return is_ok

    @property
    def transformers(self):
        return self._transformers

    def __init__(self, *args, **kwargs):
        transforms = kwargs.get('transforms')
        if transforms is None and len(args) == 0:
            raise ValueError('Please pass transforms arguments')
        transforms = args[0]

        if isinstance(transforms, list):
            is_ok = self._check_list_of_transforms(transforms)
        else:
            is_ok = False

        if not is_ok:
            raise TypeError('Wrong value shape of data')

        self._transformers = transforms

    def fit(self, X, **kwargs):
        transforms_buf = []

        for t in self._transformers:
            if len(t) == 2:
                t_name, transformer = t
                cols = None
            else:
                t_name, transformer, cols = t

            transforms_buf.append(
                (t_name, transformer.fit(X), cols)
            )

        self._transformers = transforms_buf

        return self

    def transform(self, X):
        transformed_X = X.copy()
        for t_name, t, cols in self._transformers:
            transformed_X = t.transform(transformed_X, columns=cols)

        return transformed_X
