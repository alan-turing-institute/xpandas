from sklearn.pipeline import Pipeline

from ...data_container import MultiDataFrame, MultiSeries


class PipeLineChain(Pipeline):
    '''
    PipeLine transformer. Can chain multiple transformers and estimator from scikit-learn.
    Based on scikit-learn Pipeline
    http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline
    '''

    def transform(self, X, **kwargs):
        transformed_object = super(PipeLineChain, self).transform(X, **kwargs)
        if type(transformed_object) != MultiSeries and type(transformed_object) != MultiDataFrame:
            transformed_object = MultiDataFrame(transformed_object)
        return transformed_object
