[![Build Status](https://travis-ci.org/alan-turing-institute/xpandas.svg?branch=master)](https://travis-ci.org/alan-turing-institute/xpandas)

![Logo](/examples/imgs/Logo.png)

**XPandas** (extended [`Pandas`](https://pandas.pydata.org/)) implements 1D and 2D data containers for storing type-heterogeneous tabular data of any type, 
and encapsulates feature extraction and transformation modelling in an sklearn-compatible transformer interface.

## Documentation

The full documentation is available at [https://alan-turing-institute.github.io/xpandas/](https://alan-turing-institute.github.io/xpandas/).

## Requirements

XPandas' requirements are part of the [Anaconda](https://www.continuum.io/downloads) distribution. To install the requirements manually run `pip install -r requirements.txt`.

## Tests

To run tests run the command ```pytest``` in the root folder.
If anything is broken an exception will be raised; otherwise "OK" will be printed.


## Acknowledgements

- **Bernd Bischl (@berndbischl)**, who mentioned the idea of a general data container with transformers attached to columns in personal discussion with Franz Kiraly during a London visit in 2016.
- **Franz Kiraly (@fkiraly)**, who initiated and funded the project up to release, and who substantially contributed to the API design.
- **Haoran Xue (@HaoranXue)**, who, under the supervision of Franz Kiraly, earlier completed a thesis for a degree at UCL on the topic, and who wrote a similar package as part of it. No code was re-used in the creation of the XPandas package.


List of [Developers and contributors](AUTHORS.rst)


