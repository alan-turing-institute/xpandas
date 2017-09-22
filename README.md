[![Build Status](https://travis-ci.com/kiraly-group/transformers.svg?token=WzNyjqtwC8PwsMtns62p&branch=development)](https://travis-ci.com/kiraly-group/transformers)

![Logo](/examples/imgs/Logo.png)


**XPandas** project presents data containers for storing 1d/2d data of any type
 and apply transformations over them.


## Description

**XPandas** encapsulated universal 1d (`XSeries`) and 2d (`XDataFrame`) containers and
presents new transformer classes for transforming these containers. Transformers can 
do map-reduce style complex transformations but not limited to it.

`XSeries` is based on `pandas.Series` that can store objects of any type.
For example you may want to store `pandas.Series` objects inside `XSeries`.
`XSeries` can be visualised according to a schema

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

That's where `Transformer` class comes to help. Using `CustomTransformer` class one can build it's own transformer
for `XSeries` and then `DataFrameTransformer` to create transformer for `XDataFrame`. `Transformer` is 
an encapsulation for function `f: XSeries -> XSeries or XDataFrame`.

![Transformer](/examples/imgs/Transformer.png)


## Tests

To run tests use command `pytest` from the root folder.
If anything is broken, exception will be raised else "OK' is written.

## Requirements

You only need `Pandas` and `numpy` packages to be installed.
Run `pip install -r requirements.txt` or just install [Anaconda](https://www.continuum.io/downloads).
