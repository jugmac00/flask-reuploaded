Installation
============

.. code-block:: bash

    $ pip install Flask-Reuploaded


Migration guide from `Flask-Uploads`
------------------------------------

This package is a drop-in replacement of broken `flask-uploads`.
If you have used `Flask-Uploads` and want to migrate to `Flask-Reuploaded`:

.. code-block:: bash

    $ pip uninstall `Flask-Uploads`

... Then ...

.. code-block:: bash

    $ pip install `Flask-Reuploaded`

This means you do not have to change a single line of code.


Incompatibilities between Flask-Reuploaded and Flask-Uploads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As already mentioned, staying compatible with `Flask-Uploads` is one of this 
project's goals.

Nevertheless, there are the following known incompatibilities:

- the `patch_request_class` helper function has been removed;
  the function was only necessary for Flask 0.6 and earlier.
  Since then you can use Flask's own
  `MAX_CONTENT_LENGTH <https://flask.palletsprojects.com/en/1.1.x/config/#MAX_CONTENT_LENGTH>`_
  environment variable,
  so you don’t read more than this many bytes from the incoming request data.

- `autoserve` of uploaded images now has been deactivated;
  this was a poorly documented "feature", which even could have lead to 
  unwanted data disclosure. 

  if you want to activate the feature again, you need to set 
  `UPLOADS_AUTOSERVE=True`