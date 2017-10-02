from sklearn.pipeline import Pipeline

from ...data_container import XDataFrame, XSeries


class PipeLineChain(Pipeline):
    '''
    PipeLine transformer. Can chain multiple transformers and estimator from scikit-learn.
    Based on scikit-learn Pipeline
    http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline
    '''

    def transform(self, X, **kwargs):
        transformed_object = super(PipeLineChain, self).transform(X, **kwargs)
        if type(transformed_object) != XSeries and type(transformed_object) != XDataFrame:
            transformed_object = XDataFrame(transformed_object)
        return transformed_object
