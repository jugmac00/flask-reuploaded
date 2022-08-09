Explanation
===========


Upload Sets
-----------
``UploadSet`` is the main object provided by the `FlaskReuploaded` extension.
Each `UploadSet` is responsible for dealing with a set of files. You have to initialize
`UploadSet` by calling its constructor and passing it the required first
parameter `name`:

    .. code-block:: python

        photos = UploadSet(name='photos', extensions=IMAGES)

The second parameter is optional `extensions` iterable. For your convenience,
there is a ready-to-use extension iterables you can import from
`flask_uploads.extensions`. The third parameter is the :ref:`default_dest` callable that
will be discussed later.

After initializing the `UploadSet`'s, You have to call :ref:`configure_uploads`
function that builds the `UploadConfiguration` and store it in the application instance. 

Now, your `UploadSet`'s are configured, you can use the `UploadSet.save` method to
save uploaded files and the `UploadConfiguration` to serve them.

During saving and serving the uploaded files, the `UploadSet` object performs
some security checks for you.

.. _security-checks:

Security Checks
---------------

Security itself is a huge subject and you should consider designing it
seriously. The ``Flask-Reuploaded`` extension tries to help you by preventing
some common attack vectors and user errors. For example:


- Users can't upload files with filenames that start with `.` 

e.g. `.`, '..', '../../../home/{username}/.bash' or '../../my_app.wsgi'. if a
user tries to upload a file with such a filename, the file will be renamed.

- Users can't overwrite other users' files i.e., `similar filenames are suffixed by a number`.
- Users can't upload files with extension suffixes that are not allowed by the ``UploadSet``.

You are advised to read the source code to explore the mechanism of dealing
with each error/attack and you may decide to take additional actions.


Maximum Allowed File Size
-------------------------

Another security aspect that you should consider is the maximum allowed file
size. This is ``NOT`` managed by the `Flask-Reuploaded` extension.

By default, the `Flask` application will accept file uploads of any length. It is
up to your server to save the uploaded file or fill your hard drive till
raising `No space left on device` error. You can (obviously, you should) set
the maximum allowed file length by setting the ``MAX_CONTENT_LENGTH`` configuration.
After this, `Flask` will reject files that are larger than this limit.

This alone may not be enough. As uploading a thousand files of 10 MB in size
may also cause your server to crash. This aspect is outside of the scope of this
extension but worth mentioning here.


`UploadSet` `DEST` Configuration
--------------------------------

As mentioned in the :ref:`configuration`, the `UploadSet` object should
know its destination. When you call `configure_uploads` function, the
`UploadSet` tries to set its destination path by the following order:

-  `UPLOADED_[1]_DEST` where is [1] is a capitalized `UploadSet` name
-  The return value of the :ref:`default_dest` if present
-  Subdirectory in the `UPLOADS_DEFAULT_DEST` if present. The name of the
   subdirectory is the same name of the `UploadSet`
-  Raise `RuntimeError`


.. _default_dest:

``default_dest`` Callable Parameter
-----------------------------------

The `UploadSet` constructor can accept ``default_dest`` parameter, it is a callable
that takes the application as its argument and returns the destination path for
this set.

For example::

    ..code-block:: python
        
        def set_destination(app):
            return os.path.join(app.instance_path, "uploads")
            
        media = UploadSet('media', default_dest=set_destination )

This will save your uploads in the ``app.instance_path/uploads``


.. _configure_uploads:

`configure_uploads` Function
----------------------------

You have to call the `configure_uploads` function after the app has been
configured. The `configure_uploads` function is responsible for creating the
`UploadConfiguration`'s and storing them on the application instance.

Storing the `UploadConfiguration` on the application instance enables you to
get it when you need to serve the files from the `UploadSet`. The
`current_app.upload_set_config` is a dictionary of `UploadSet` names mapped to
their corresponding `UploadConfiguration` objects.

The `configure_uploads` function accepts two parameters. The first is the
`Flask` application instance and the second is either an UploadSet instance or
iterable of UploadSet instances. It is safe to call the `configure_uploads`
function more than once.


Multithreaded Application
-------------------------

As mentioned, the :ref:`configure_uploads` function stores the `UploadSet`'s
configuration on the application instance itself. That way, you can have
`UploadSet` being used by multiple applications that run in different threads. 
. If your application has a factory function, that is a good place to call it.
    
    .. code-block:: python


        from flask_uploads import configure_uploads

        def init_app():              
            ...            
            configure_uploads(app, (photos, media))
            ...
            return app


Saving Files
------------

When you upload a file, you should call the ``UploadSet.save`` method. This
method accept a ``werkzeug.datastructures.FileStorage`` object as its first parameter. Any object
with another type will raise ``TypeError``. You can get a
``werkzeug.datastructures.FileStorage`` object by accessing the 
``flask.request.files`` dictionary.

The ``UploadSet.save`` method accepts optional parameter ``folder``, if
present, the uploaded file will be saved in ``UploadSet.destination/folder``
subdirectory.

The third optional parameter is the `name`. If set, the `UploadSet` will use
this value instead of the value of the
``werkzeug.datastructures.FileStorage.filename``. 

The ``UploadSet.save`` method returns the saved filename. Note that the saved
`filename` isn't always equal to the `filename` uploaded by the
user. As  mentioned in :ref:`security-checks`, The `Flask-Reuploaded`
extension might rename the uploaded file in certain circumstances. Also, if you pass the
``folder`` parameter the return value will be a relative path to the
`UploadSet` destination.

You are expected to store the saved `filename` name in order to use it for
serving the uploaded file later. 


File Upload Forms
-----------------

To actually upload the files, you need to properly set up your requests. You
need to pass a ``werkzeug.datastructures.FileStorage`` object to the
`UploadSet.save` method. You can get this object by accessing the
``flask.request.files['field_name']`` where `field_type` is equal to the field
name of the uploaded file in your form.

Unfortunately, the ``flask.request.files['field_name']`` may be empty if your
request is misconfigured. As declared by Flask_:
    
    Note that files will only contain data if the request method was POST, PUT
    or PATCH and the <form> that posted to the request had
    enctype="multipart/form-data". It will be empty otherwise. 

.. _Flask: https://flask.palletsprojects.com/en/2.1.x/api/#flask.Request.files

This means that if the request method is `GET`, it won't work at all, and
if you don't set the enctype, only the filename will be transferred.

The field in the `HTML` form itself should be an ``<input type='file'>``. For
example: 

.. code-block:: html+jinja

    <form method=POST enctype=multipart/form-data action="{{ url_for('upload') }}">
        ...
        <input type='file' name='photo'>
        <!-- Your application will receive the uploaded file in -->
        <!-- `request.files['photo']`  -->
        ...
    </form>

If you are using a client other than the browser, you should configure your
request manually to implement the flask requirements.


Serving Files
-------------

When you upload file by `Flask-Reuploaded` extension, you call the
``UploadSet.save`` method. this method returns the saved `filename`. You are
expected to store the saved `filename` and the `UploadSet` name in order to use
them for serving the uploaded file later. 

To serve an uploaded file, use the `UploadSet` name to get the
`UploadConfiguration` instance:

    .. code-block:: python
        
        uploadset_config = current_app.upload_set_config.get(uploadset_name)

If the `uploadset_config` is not `None`, you can pass its `destination`
property as well as the saved `filename` to the ``flask.send_from_directory`` method to
safely serve your file.
    
    .. code-block:: python

        return send_from_directory(uploadset_config.destination, filename)


AutoServing Files
-----------------

To save your time, you can set `app.config['UPLOADS_AUTOSERVE']` to `True`.
This will add `_uploads.uploaded_file` endpoint to your application. This
endpoint requires two parameters, `setname` parameter which should be equal to
the `UploadSet` name and the `filename` parameter which is the saved
`filename`.

Once you have these parameters, you can serve your uploaded files from this url:

    .. code-block:: python

        url =  url_for(
            "_uploads.uploaded_file", setname="photos", filename=filename
        )

Note that the ``UPLOADS_AUTOSERVE`` is `True` by default in
``Flask-Reuploaded<1.0.0`` and `False` by default in the next versions.

