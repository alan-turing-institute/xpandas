![Logo](/examples/imgs/Logo.png)

[![Build Status](https://travis-ci.com/kiraly-group/XPandas.svg?token=WzNyjqtwC8PwsMtns62p&branch=master)](https://travis-ci.com/kiraly-group/transformers)


**XPandas** project presents data containers for storing 1d/2d data of any type
 and apply transformations over them.


## Description

**XPandas** encapsulated universal 1d (`XSeries`) and 2d (`XDataFrame`) containers and
presents new transformer classes for transforming these containers. Transformers can 
do map-reduce style complex transformations but not limited to it.

`XSeries` is based on `pandas.Series` that can store objects of any type.
For example you may want to store `pandas.Series` objects inside `XSeries`.
`XSeries` can be visualised according to a schema

![XSeries](/examples/imgs/XSeries.png =250x250)


## Tests

To run tests use command ```python``` from the root folder.
If anything is broken, exception will be raised else "OK' is written.

## Requirements

You only need `Pandas` and `numpy` packages to be installed.
Run `pip install -r requirements.txt` or just install [Anaconda](https://www.continuum.io/downloads).

## Test section