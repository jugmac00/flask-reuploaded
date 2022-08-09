Installation
============

.. code-block:: bash

    $ pip install Flask-Reuploaded


.. _migration-guide:

Migration Guide From 'Flask-Uploads'
------------------------------------

This package is a drop-in replacement of unmaintained `Flask-Uploads`.
If you have used `Flask-Uploads` and want to migrate to `Flask-Reuploaded`:

.. code-block:: bash

    $ pip uninstall `Flask-Uploads`

... then ...

.. code-block:: bash

    $ pip install `Flask-Reuploaded`

This means you do not have to change a single line of code.


Incompatibilities Between Flask-Reuploaded and Flask-Uploads
------------------------------------------------------------

As already mentioned, staying compatible with `Flask-Uploads` is one of this 
project's goals.

Nevertheless, there are the following known incompatibilities:

- The `patch_request_class` helper function has been removed;
  the function was only necessary for Flask 0.6 and earlier.
  Since then, you can use Flask's own
  `MAX_CONTENT_LENGTH <https://flask.palletsprojects.com/en/1.1.x/config/#MAX_CONTENT_LENGTH>`_
  configuration variable, so you don’t read more than this many bytes from the incoming request data.

- `UPLOADS_AUTOSERVE` of uploaded images has now been deactivated;
  this was a poorly documented "feature", which even could have led to 
  unwanted data disclosure. 

  If you want to activate the feature again, you need to set 
  `UPLOADS_AUTOSERVE=True`
