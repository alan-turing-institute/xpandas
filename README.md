This repository presents new model for storing 2d data of any type in Python.
Inspired by Pandas.


## Description

This module encapsulated universal 1d (`XSeries`) and 2d (`XDataFrame`) containers and
presents new transformer classes for transforming these containers.

`XSeries` is a 1d based on pandas.Series that can store objects of any type.
For example you may want to store `pandas.Series` objects inside `XSeries`.
`XSeries` can be visualised according to a schema

![XSeries](/examples/imgs/XSeries.png)


[![Build Status](https://travis-ci.com/kiraly-group/XPandas.svg?token=WzNyjqtwC8PwsMtns62p&branch=master)](https://travis-ci.com/kiraly-group/transformers)

## Tests

To run tests use command ```python``` from the root folder.
If anything is broken, exception will be raised else "OK' is written.

## Requirements

You only need `Pandas` and `numpy` packages to be installed.
Run `pip install -r requirements.txt` or just install [Anaconda](https://www.continuum.io/downloads).

## Test section