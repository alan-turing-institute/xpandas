[![Build Status](https://travis-ci.com/kiraly-group/XPandas.svg?token=WzNyjqtwC8PwsMtns62p&branch=development)](https://travis-ci.com/kiraly-group/XPandas)

![Logo](/examples/imgs/Logo.png)

**XPandas** (extended [`Pandas`](https://pandas.pydata.org/)) project presents data containers for storing 1d/2d data of any type and apply transformations over them.

## Examples

Take a look at `examples/Example Usage.ipynb` for understanding basic functionality of `XPandas`.

## Requirements

XPandas' requirements are part of the [Anaconda](https://www.continuum.io/downloads) distribution. To install the requirements manually run `pip install -r requirements.txt`.

## Description

**XPandas** encapsulated universal 1d (`XSeries`) and 2d (`XDataFrame`) containers and
presents new transformer classes for transforming these containers. Transformers can 
do map-reduce style complex transformations but not limited to it.

`XSeries` is based on `pandas.Series` that can store objects of any type.
For example you may want to store `pandas.Series` objects inside `XSeries`.
`XSeries` can be visualised according to a schema.

![XSeries](/examples/imgs/XSeries.png)

`XDataFrame` is based on `pandas.DataFrame` and can store set of `XSeries`. One can imagine a data set 
of a patients in hospital. There might be features like numbers (age, height, weight, etc.), categorical (gender,
hair color, etc.), images (patients x-ray pictures), time series (heat beat over time), and any other.
Using `XDataFrame` one can store all this information into one in memory 2d container.

![XDataFrame](/examples/imgs/XDataFrame.png)

Ones one has such a complex data set usually to use some ready-to-go machine learning algorithm like in 
[scikit-learn](scikit-learn.org) one needs a quantitative features. Thus, the next task is to extract features
from columns of `XDataFrame`. In example with patients data, one may want to extract stats features from 
each `pandas.Series` or extract features from each images using fancy deep learning model.

That's where `Transformer` class comes to help. Using `XSeriesTransformer` class one can build it's own transformer
for `XSeries` and then `XDataFrameTransformer` to create transformer for `XDataFrame`. `Transformer` is 
an encapsulation for function `f: XSeries -> XSeries or XDataFrame`.

![Transformer](/examples/imgs/Transformer.png)

There are several pre implementer transformers that may be useful for several data types:

###### Time series
* `TimeSeriesTransformer(features)` — extract `features` from each series.
`features` is a subset of [
        'mean', 'std', 'max', 'min',
        'median', 'quantile_25', 'quantile_75',
        'quantile_90', 'quantile_95'
    ]

* `TimeSeriesWindowTransformer(windows_size)` — calculate rolling mean with given `windows_size`
* `TsFreshSeriesTransformer` — extract features using [tsfresh](tsfresh.readthedocs.io) package


###### Image
* `ImageTransformer` — Performs image transformation based on 
skimage
[transformation function](http://scikit-image.org/docs/dev/api/skimage.transform.html)


###### Categorical data
* `BagOfWordsTransformer(dictionary)` —
Performs bag-of-features transformer for strings of any categorical data


There is also a special transformer called `PipeLineChain`. This transformer can
chain multiple transformers and `scikit-learn` predictor into a single pipeline.
`PipeLineChain` is based on `scikit-learn`
[Pipeline](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline).

## Tests

To run tests run the command ```nosetests tests``` in the root folder.
If anything is broken an exception will be raised; otherwise "OK" will be printed.
