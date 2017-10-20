import numpy as np
import skimage.transform as skimage_transform

from ..xpandas.data_container import XSeries
from ..xpandas.transformers.image_transformer import ImageTransformer

n = 20
m = 20
colours_n = 255


def generate_image(is_3d=True):
    if is_3d:
        return (np.random.rand(30, 30, 3) * 255).astype('uint8')
    return (np.random.rand(30, 30) * 255).astype('uint8')


def test_image_transformation():
    s = XSeries([generate_image(False) for _ in range(100)])

    try:
        image_transformer = ImageTransformer().fit()
        assert False
    except:
        assert True

    image_transformer = ImageTransformer(skimage_transform.hough_circle, radius=5).fit()
    s_transformed = image_transformer.transform(s)

    assert s_transformed.data_type == np.ndarray

    image_transformer = ImageTransformer(skimage_transform.resize, output_shape=(10, 10)).fit()
    s_transformed = image_transformer.transform(s)

    assert s_transformed.data_type == np.ndarray
