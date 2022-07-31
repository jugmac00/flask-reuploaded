Explanantion
=============

..
  This section requires more improvements.


Upload Sets
===========
An `UploadSet` is a single collection of files.
You just declare them in the code::

    photos = UploadSet('photos', IMAGES)

And then you can use the `UploadSet.save` method to save uploaded files and
`UploadSet.path` and `UploadSet.url` to access them.

If you have a "default location" for storing uploads - for example, if your
app has an "instance" directory and uploads should be saved to
the instance directory's ``uploads`` folder - you can pass a ``default_dest``
callable to the set constructor. It takes the application as its argument.
For example::

    media = UploadSet('media', default_dest=lambda app: app.instance_path)

This won't prevent a different destination from being set in the config,
though. It's just to save your users a little configuration time.


App Configuration
=================

An `UploadSet`'s configuration is stored on an app. That way, you can have
upload sets being used by multiple apps at once. You use the
`configure_uploads` function to load the configuration for the `UploadSet`s.
You pass in the app and all of the `UploadSet`s you want configured. Calling
`configure_uploads` more than once is safe. ::

    configure_uploads(app, (photos, media))

If your app has a factory function, that is a good place to call this
function.


File Upload Forms
=================

To actually upload the files, you need to properly set up your form. A form
that uploads files needs to have its method set to POST and its enctype
set to ``multipart/form-data``. If it's set to GET, it won't work at all, and
if you don't set the enctype, only the filename will be transferred.

The field itself should be an ``<input type=file>``.

.. code-block:: html+jinja

    <form method=POST enctype=multipart/form-data action="{{ url_for('upload') }}">
        ...
        <input type=file name=photo>
        ...
    </form>
