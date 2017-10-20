[![Build Status](https://travis-ci.org/kiraly-group/xpandas.svg?branch=master)](https://travis-ci.org/kiraly-group/xpandas)

![Logo](/examples/imgs/Logo.png)

**XPandas** (extended [`Pandas`](https://pandas.pydata.org/)) implements 1D and 2D data containers for storing type-heterogeneous tabular data of any type, 
and encapsulates feature extraction and transformation modelling in an sklearn-compatible transformer interface.

## Documentation

Please read the user documentation for understanding basic functionality of `XPandas`. To build the docs run ``make html`` from the [docs directory](/docs).

## Requirements

XPandas' requirements are part of the [Anaconda](https://www.continuum.io/downloads) distribution. To install the requirements manually run `pip install -r requirements.txt`.

## Description

**XPandas** provides universal 1D typed list (`XSeries`) and 2D type-heterogeneous data-frame (`XDataFrame`) containers
and provides an extended sklearn-like transformer classes interfacing said containers. 
Transformers can be used for automated feature extraction and map-reduce style transformations but are not limited to it.

`XSeries` is based on `pandas.Series` that can store objects of any type.
Example would be a series of image containers, or a series of `pandas.Series` objects stored as `XSeries`.
`XSeries` can be visualised according to a schema.

![XSeries](/examples/imgs/XSeries.png)

`XDataFrame` extends `pandas.DataFrame` by allowing arbitrary object types per column.
It provides the same convenient sub-setting interface and extended abstract access methods.
Each column is internally stored as an `XSeries` container, all of same length. 
One example could be a medical data set where each row is a different patient, say, in a hospital. 
The columns would correspond to a type-heterogeneous set of features like numbers (age, height, weight, etc.), 
categorical (gender, hair color, etc.), images (x-ray pictures), time series (heat beat, lab history), 
and other parts of a medical record.
With `XDataFrame` one can store all this information in a single 2D data container instead of a tedious collection of custom nested lists or arrays.

![XDataFrame](/examples/imgs/XDataFrame.png)

Another advantage of XPandas is the clean interface it provides to ready-to-go machine learning algorithms in 
[scikit-learn](scikit-learn.org). The transformers interface can be used to easily convert the types in a `XDataFrame`
to the primitive types with which sklearn can interface, as part of a modelling pipeline. 
In the example with patients data, one may want to extract summary features from 
each `pandas.Series`, or extract features from each image, say via a fancy deep learning model.

More technically, the implemented `XSeriesTransformer` class allows implementation of transformation defaults
for `XSeries`, similarly `XDataFrameTransformer` implements transforation for `XDataFrame` type objects. 
More mathematically `XSeriesTransformer` encapsulates abstract functions of type `XSeries -> XSeries or XDataFrame`,
`XDataFrameTransformer` encaplsulates functions `XDataFrame -> XDataFrame`, both following the familiar fit/transform/parameters API from sklearn.

![Transformer](/examples/imgs/Transformer.png)

XPandas comes with several pre-implemented transformers for the most common non-primitive data types:

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


XPandas also allows for pipelining, via the `PipeLineChain` transformer, which can
chain multiple transformers and `scikit-learn` predictor into a single pipeline.
`PipeLineChain` is based on the `scikit-learn`
[Pipeline](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline).

## Tests

To run tests run the command ```pytest``` in the root folder.
If anything is broken an exception will be raised; otherwise "OK" will be printed.


## Acknowledgements

- **Bernd Bischl (@berndbischl)**, who mentioned the idea of a general data container with transformers attached to columns in personal discussion with Franz Kiraly during a London visit in 2016.
- **Franz Kiraly (@fkiraly)**, who initiated and funded the project up to release, and who substantially contributed to the API design.
- **Haoran Xue (@HaoranXue)**, who, under the supervision of Franz Kiraly, earlier completed a thesis for a degree at UCL on the topic, and who wrote a similar package as part of it. No code was re-used in the creation of the XPandas package.


## Developers and contributors

Current:
- **Vitaly Davydov [iwitaly](https://github.com/iwitaly)**: principal developer and curator
- **Franz Kiraly [fkiraly](https://github.com/fkiraly)**: project manager and designated point of contact
- **Frithjof Gressmann [frthjf](https://github.com/frthjf)**: contributor

Former/inactive:
none
