Installation
************

The installation of the latest stable version is easy using the python package manager `pip`_. ::

    pip install xpandas

That's it. You are now ready to go. We recommend reading the :doc:`/user_guide` to get started.

Bleeding edge
^^^^^^^^^^^^^

To test or develop new features you may want to install the latest package version from the master branch (bleeding edge installation).

Clone the source from our `public code repository`_ on GitHub and change into the XPandas directory. Make sure that all dependencies are installed ::

    pip install -r requirements.txt

Then run ::

    python setup.py develop

to install the package into the activated Python environment. To build the documentation run ::

    cd docs/ && make html

Note that bleeding edge installations are likely contain bugs are not recommended for productive environments.


.. _pip: http://www.pip-installer.org/
.. _public code repository: https://github.com/kiraly-group/XPandas