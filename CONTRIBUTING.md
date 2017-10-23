## How to contribute to xpandas

#### **Did you find a bug?**

* **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/kiraly-group/xpandas/issues).

* If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/kiraly-group/xpandas/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

* Please follow the further discussion in case more information is needed or questions arise.

#### **Did you write a patch that fixes a bug?**

* Open a new GitHub pull request with the patch.

* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

#### **Do you intend to add a new feature or change an existing one?**

* Suggest your change in an issue and offer to implement the feature. 

* Wait for positive feedback in order to avoid double work (maybe your idea is already in development).

* Implement and send a PR

#### **Do you want to contribute to the xpandas documentation?**

* Understand how the documentation is build (see below)
* Send a PR that propose changes to the docs directory

We use a custom [Makefile](docs/Makefile) that configures an automatic generation of the `*.rst` API documentation of each entity (class or module) in the [docs/api](docs/api) directory:

    buildapi:
        sphinx-apidoc -fMeT ../xpandas -o api
        @echo "Auto-generation of API documentation finished. " \
              "The generated files are in 'api/'"

Before building the documentation the entity files have therefore to be regenerated from the source using the `make buildapi` command. Then, `make html` creates the HTML documentation which includes a conversion of the [examples notebook](examples/ExampleUsage.ipynb) into *ExampleUsage.rst* before building.

**Deployment of the documentation**

This documenation is hosted on GitHub Pages instead of [ReadTheDocs](https://readthedocs.org/) to avoid adverts and keep all things together on Github.

As GitHub Pages does not support Sphinx we make us of the [Doctr](https://drdoctr.github.io/doctr/) package that automatically updates our docs
on GH Pages branch using Travis CI; the build process is triggered by commits to the master branch that pass the tests. Please take a look at the [.travis.yml](.travis.yml) file for more details.
 
XPandas is a team effort. We encourage you to pitch in and join us!

Thanks! :heart: :heart: :heart:

Xpandas Team
