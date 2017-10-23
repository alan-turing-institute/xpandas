Contributions
+++++++++++++++


How to build the docs?
=======================

If you take a look at *Makefile* in the repository you find out that
there is a custom command ::

    buildapi:
        sphinx-apidoc -fMeT ../xpandas -o api
        @echo "Auto-generation of API documentation finished. " \
              "The generated files are in 'api/'"


This command generates a list of *.rst* files in *docs/api* folder. Each file
documents entity (class or module) of **XPandas** package.

Thus, before building documentation one has to regenerate entity files with a command
``make buildapi``.


After this run ``make html``. This command is also have been changed from default.
Before actually building Sphinx docs it converts `examples/ExampleUsage.ipynb` into
*ExampleUsage.rst* file and then performs building. **YES, ExampleUsage.ipynb name is hardcoded!**.



How to deploy docs?
=======================

This docs are hosted on Github Pages. The question is how and why?

One can easily host docs using `READTHEDOCS <https://readthedocs.org/>`_ service.
But this service is paid and thus they put ads banner on your website. Plus
it feels more *natively* to host everything on Github.

Natively GH Pages doesn't support Sphinx docs. In order to host it, one needs
to use `Doctr <https://drdoctr.github.io/doctr/>`_ package.
`Doctr <https://drdoctr.github.io/doctr/>`_ automatically update
your docs on GH Pages using Travis-CI if it hasn't failed running
tests on a `master` branch. Please take a look at ``.travis.yml`` file for settings.


