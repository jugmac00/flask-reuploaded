.. image:: https://github.com/jugmac00/flask-reuploaded/workflows/CI/badge.svg?branch=master
   :target: https://github.com/jugmac00/flask-reuploaded/actions?workflow=CI
   :alt: CI Status

.. image:: https://coveralls.io/repos/github/jugmac00/flask-reuploaded/badge.svg?branch=master
    :target: https://coveralls.io/github/jugmac00/flask-reuploaded?branch=master

.. image:: https://img.shields.io/pypi/v/flask-reuploaded   
    :alt: PyPI
    :target: https://github.com/jugmac00/flask-reuploaded

.. image:: https://img.shields.io/pypi/pyversions/flask-reuploaded   
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/Flask-Reuploaded/

.. image:: https://img.shields.io/pypi/l/hibpcli
    :target: https://github.com/jugmac00/flask-reuploaded/blob/master/LICENSE


Flask-Reuploaded
================

*Flask-Reuploaded Provides file uploads for Flask.*

Installation
------------

.. code-block:: bash

    $ pip install `Flask-Reuploaded`


Notes on this package
---------------------

This is an independently maintained version of `Flask-Uploads`
including four years of unreleased changes, at least not released to PyPI.

Noteworthy is the fix for the `Werkzeug` API change.
Please see the migration guide from `flask-uploads`


Goals
-----

- provide a stable drop-in replacement for `Flask-Uploads`
- regain momentum for this widely used package
- provide working PyPI packages


Links:
------
- documentation: https://flask-reuploaded.readthedocs.io/
- Source: https://github.com/jugmac00/flask-reuploaded
- Pypi: https://pypi.org/project/Flask-Reuploaded/
- Example Application [Examples](examples/example.rst)


Documentation
-------------

You can find the documentation at:

https://flask-reuploaded.readthedocs.io/en/latest/

You can generate the documentation locally:

.. code-block:: bash

    tox -e docs

You can update the dependencies for documentation generation:

.. code-block:: bash

    tox -e upgradedocs



Contributing
------------

Contributions are more than welcome.

Please have a look at the `open issues <https://github.com/jugmac00/flask-reuploaded/issues>`_.

There is also a `short contributing guide <https://github.com/jugmac00/flask-reuploaded/blob/master/CONTRIBUTING.rst>`_.
