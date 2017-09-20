from sklearn.pipeline import Pipeline

from ...data_container import MultiDataFrame, MultiSeries


class PipeLineChain(Pipeline):
    def transform(self, X, **kwargs):
        transformed_object = super(PipeLineChain, self).transform(X, **kwargs)
        if type(transformed_object) != MultiSeries and type(transformed_object) != MultiDataFrame:
            transformed_object = MultiDataFrame(transformed_object)
        return transformed_object


        # def _check_list_of_transforms(self, transforms):
        #     try:
        #         is_ok = all(
        #             len(t) > 1 and type(t[0]) == str
        #             for t in transforms
        #         )
        #     except:
        #         is_ok = False
        #     return is_ok
        #
        # @property
        # def transformers(self):
        #     return self._transformers
        #
        # def __init__(self, *args, **kwargs):
        #     '''
        #     transforms: list of tuples (transformer_name, transformer_object, columns_to_apply)
        #     :param args:
        #     :param kwargs:
        #     '''
        #     transforms = kwargs.get('transforms')
        #     if transforms is None and len(args) == 0:
        #         raise ValueError('Please pass transforms arguments')
        #     transforms = args[0]
        #
        #     if isinstance(transforms, list):
        #         is_ok = self._check_list_of_transforms(transforms)
        #     else:
        #         is_ok = False
        #
        #     if not is_ok:
        #         raise TypeError('Wrong value shape of data')
        #
        #     self._transformers = transforms
        #
        # def fit(self, X, **kwargs):
        #     self._transformation_steps = [X]
        #
        #     for i, (t_name, transformer) in enumerate(self._transformers):
        #         data_to_fit_transform = self._transformation_steps[i]
        #
        #         transformer.fit(
        #             data_to_fit_transform, **kwargs
        #         )
        #
        #         self._transformation_steps.append(
        #             transformer.transform(data_to_fit_transform)
        #         )
        #
        #     return self
        #
        # def transform(self, X):
        #     transformed_X = X.copy()
        #     transformed_X.name = X.name
        #
        #     for t_name, t in self._transformers:
        #         transformed_X = t.transform(transformed_X)
        #
        #     if type(transformed_X) != MultiSeries and type(transformed_X) != MultiDataFrame:
        #         transformed_X = MultiDataFrame(transformed_X)
        #
        #     return transformed_X
