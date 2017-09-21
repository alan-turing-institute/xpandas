from sklearn.pipeline import Pipeline

from ...data_container import MultiDataFrame, MultiSeries


class PipeLineChain(Pipeline):
    def transform(self, X, **kwargs):
        transformed_object = super(PipeLineChain, self).transform(X, **kwargs)
        if type(transformed_object) != MultiSeries and type(transformed_object) != MultiDataFrame:
            transformed_object = MultiDataFrame(transformed_object)
        return transformed_object
