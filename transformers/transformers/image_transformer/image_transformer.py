import numpy as np

from ..transformer import CustomTransformer


class ImageTransformer(CustomTransformer):
    def __init__(self, skimage_function=None, **function_params):
        accepted_types = [
            list, np.ndarray, np.array
        ]

        if skimage_function is None:
            raise Exception('Please specify transform function from scikit-image'
                            ' http://scikit-image.org/docs/dev/api/skimage.transform.html')

        def image_transform_function(img):
            return skimage_function(img, **function_params)

        super(ImageTransformer, self).__init__(data_types=accepted_types,
                                               columns=None,
                                               transform_function=image_transform_function)
