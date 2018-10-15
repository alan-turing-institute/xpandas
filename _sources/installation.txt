Installation
************

Stable
^^^^^^^^^^^^^

The installation of the latest stable version is easy using the python package manager `pip`_. ::

    pip install xpandas

That's it. You are now ready to go. We recommend reading the :doc:`examples <ExampleUsage>` to get started.


Bleeding edge
^^^^^^^^^^^^^

To test or develop new features you may want to install the latest package version
from the master branch (bleeding edge installation). You can install directly from Git repository ::

    pip install git+https://github.com/alan-turing-institute/xpandas.git


Or clone the source from our `public code repository`_ on GitHub and change into the XPandas directory.
Make sure that all dependencies are installed ::

    pip install -r requirements.txt

Then run ::

    python setup.py develop

to install the package into the activated Python environment.
If you would like to contribute to documentation please refer to :ref:`Contributing`.

Note that bleeding edge installations are likely contain bugs are not recommended for productive environments.


.. _pip: http://www.pip-installer.org/
.. _public code repository: https://github.com/alan-turing-institute/xpandas