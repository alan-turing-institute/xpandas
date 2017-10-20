import numpy as np

from ..transformer import XSeriesTransformer


class IdentityTransformer(XSeriesTransformer):
    '''
    Performs identity transformer X -> X
    '''
    def __init__(self):
        super(IdentityTransformer, self).__init__(transform_function=lambda x: x)
