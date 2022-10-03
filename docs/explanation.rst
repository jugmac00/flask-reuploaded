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
there are ready-to-use extensions you can import from
`flask_uploads.extensions`. 
The third parameter is the :ref:`default_dest` callable that
will be discussed later.

After initializing the `UploadSet`, you have to call :ref:`configure_uploads`
function that builds the `UploadConfiguration` and stores it on the application instance. 

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


- Users can't upload files with filenames that start with dot `.` for example:
    a. '.' 
    b. '..'
    c. '../../../home/{username}/.bash'
    d. '../../my_app.wsgi'

if a user tries to upload a file with such a filename, the file will be renamed.

- Users can't overwrite other users' files, i.e., `similar filenames are suffixed by a number`.
- Users can't upload files with extension suffixes that are not allowed by the ``UploadSet``.

You are advised to read the source code to explore the mechanism of dealing
with each error/attack, and you may decide to take additional actions.


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


Configuring the destination for ``UploadSet``s
----------------------------------------------

Each ``UploadSet`` object should know its destination path to store the uploaded
files in. When you call the ``configure_uploads`` function, the ``UploadSet`` object
tries to set its destination path following this order:

-  ``UPLOADED_[1]_DEST`` where is ``[1]`` is the capitalized name of the ``UploadSet``
-  The return value of the :ref:``default_dest`` if present
-  Subdirectory in the ``UPLOADS_DEFAULT_DEST`` if present. The name of the
   subdirectory is the same name of the `UploadSet`

If all these trials failed, a ``RuntimeError`` will be raised.

.. _default_dest:

``default_dest`` 
----------------

The `UploadSet` constructor can accept a ``default_dest`` parameter. It is a callable
that takes the application as its argument and returns the destination path for
this set.

For example::

    ..code-block:: python
        
        def set_destination(app):
            return os.path.join(app.instance_path, "uploads")
            
        media = UploadSet('media', default_dest=set_destination )

This will save your uploads in the ``<app.instance_path>/uploads``.


.. _configure_uploads:

`configure_uploads`
-------------------

You have to call the ``configure_uploads`` function after the app has been
configured. The ``configure_uploads`` function is responsible for creating the
``UploadConfiguration``'s and storing them on the application instance.

The ``configure_uploads`` function accepts two parameters. The first is the
`Flask` application instance and the second is either an ``UploadSet`` instance 
or iterable of UploadSet instances. It is safe to call the ``configure_uploads``
function more than once.

The ``configure_uploads`` function sets ``upload_set_config`` attribute on the
application instance. It is a dictionary of ``UploadSet`` names mapped to
their corresponding ``UploadConfiguration`` objects. This way, you are able to
get the ``UploadConfiguration`` in your view functions from
``current_app.upload_set_config['setname']`` when you need to serve the files,
see :ref:`serving_files`. 


Multithreaded Application
-------------------------

As mentioned, the :ref:``configure_uploads`` function stores the ``UploadSet``'s
configuration on the application instance itself. That way, you can have
``UploadSet`` being used by multiple applications that run in different threads. 
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
method accepts a ``werkzeug.datastructures.FileStorage`` object as its first parameter. Any object
with another type will raise ``TypeError``. You can get a
``werkzeug.datastructures.FileStorage`` object by accessing the 
``flask.request.files`` dictionary.

The ``UploadSet.save`` method accepts optional parameter ``folder``. If
given, the uploaded file will be saved in ``UploadSet.destination/folder``
subdirectory.

The third optional parameter is the ``name``. If given, the ``UploadSet`` will use
this value instead of the value of the
``werkzeug.datastructures.FileStorage.filename``.

Note that you can include the ``folder`` in the ``name`` parameter  instead of
explicitly using ``folder``, i.e. ``uset.save(file, name="someguy/photo_123.")``

By using the ``folder`` and ``name`` parameters, You can achieve complete control
of the saved files within the ``UploadSet``. As an example: you can store each
user files in a separate directory. 

The ``UploadSet.save`` method returns the saved filename. Note that this isn't
always equal to the ``filename`` uploaded by the user nor the ``name`` parameter
you passed. As mentioned in :ref:`security-checks`, the `Flask-Reuploaded`
extension might rename the uploaded file in certain circumstances. Also, if you
pass the ``folder`` parameter the return value will be a relative path to the
``UploadSet`` destination.

Usually, you are expected to store the return value of the ``UploadSet.save``
method  in order to use it for serving the uploaded file later. 


File Upload Forms
-----------------

To actually upload the files, you need to properly set up the `HTTP` requests.
You must obtain a ``werkzeug.datastructures.FileStorage`` by using the
``flask.request.files['field_name']``.

Unfortunately, the ``flask.request.files['field_name']`` may be empty if your
request is misconfigured. As declared by Flask_:
    
    Note that files will only contain data if the request method was POST, PUT
    or PATCH and the <form> that posted to the request had
    enctype="multipart/form-data". It will be empty otherwise. 

.. _Flask: https://flask.palletsprojects.com/en/latest/api/#flask.Request.files

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
request manually to implement the Flask's requirements.


.. _serving_files:

Serving Files
-------------

When you upload a file using the `Flask-Reuploaded` extension, you call the
``UploadSet.save`` method. This method returns the saved ``filename`` or path. You are
expected to store the `UploadSet` name and the ``UploadSet.save`` return value
for serving the uploaded file. 

To serve an uploaded file, use the ``UploadSet`` name to get the
``UploadConfiguration`` instance:

    .. code-block:: python
        
        uploadset_config = current_app.upload_set_config.get(uploadset_name)

If the ``uploadset_config`` is not ``None``, you can pass its ``destination``
property as well as the saved ``filename`` to the ``flask.send_from_directory`` method to
safely serve your file.
    
    .. code-block:: python

        return send_from_directory(uploadset_config.destination, filename)

Of course, you can use another method, but the ``send_from_directory`` is secure
and it uses ``flask.send_file`` under the hood. Please take a look at the
send_from_directory_ and send_file_ .

.. _send_from_directory: https://flask.palletsprojects.com/en/latest/api/#flask.send_from_directory
.. _send_file: https://flask.palletsprojects.com/en/latest/api/#flask.send_file



AutoServing Files
-----------------

You can save time, you can set ``app.config['UPLOADS_AUTOSERVE']`` to ``True``.
This will add ``_uploads.uploaded_file`` endpoint to your application. This
endpoint requires two parameters, ``setname`` parameter, which should be equal to
the ``UploadSet`` name; and the ``filename`` parameter, which is the saved ``filename``
or path, i.e., the return value of the ``UploadSet.save`` method.

Once you have these parameters, you can serve your uploaded files from this url:

    .. code-block:: python

        url =  url_for(
            "_uploads.uploaded_file", setname="photos", filename=filename
        )

Note that the ``UPLOADS_AUTOSERVE`` is ``True`` by default in
``Flask-Reuploaded<1.0.0`` and `False` by default in all higher versions.

