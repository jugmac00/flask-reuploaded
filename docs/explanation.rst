Explanantion
=============

..
  This section requires more improvements.


Upload Sets
-----------
``UploadSet`` is The main object provided by this extension. Each `UploadSet` is
responsible for dealing with set of files. You declare `UploadSet` in the code::

    photos = UploadSet('photos', IMAGES)

And then you can use the `UploadSet.save` method to save uploaded files and
`UploadSet.path` and `UploadSet.url` to access them.

during saving & retrieving the uploaded file, `UploadSet` perform some security
checks for you.


Security Checks:
----------------

Security itself is a huge subject and you should consider designing it
seriously. This extension is not intended by first intention to protect your
app. However ``Flask-Reuploaded`` extension tries to help you in preveting the
common simple attacks or user errors. for Example::

    - User can't upload file with filename that starts with `.` 
      This means that user can't upload `.`, '..', '../../../home/{username}/.bash' or '../../my_app.wsgi'.
      i.e:. filename will cahnged or internal server error will be raised.
    - User can't overwrite other users files i.e:. `similar filenames are suffixed by number`
    - User can't upload file with extension suffix that is not allowed by the ``UploadSet``.

You are adviced to read the source code to explore the mechanism of dealing with
each error/attack and you may decide to fix something yourself.

Another security aspect that you should consider is the maximum allowed file
size. This is ``NOT`` managed by `Flask-Reuploaded` extension nor the `Flask`
itself.

By default `Flask` will happily accept one hundred GB file upload till crashing your hard
drive by `no empty space error`. You can set maximum length by setting
``MAX_CONTENT_LENGTH`` configuration. after this `flask` will reject files that
are more than this limit.

This is alone may not be enough. As uploading one thousand files of 10 MB length
will crash your server also. This aspects is out of the scope of this extension
but worth mentioned here.




Default Dest Callable Parameter:
--------------------------------

`UploadSet` constructor can accept ``default_dest`` parameter, it is callable
that takes the application as its argument & returns the destination path for
this set.

For example::

    .. code-block:: python

        media = UploadSet('media', default_dest=lambda app: os.path.join(app.instance_path, "uploads"))

This will save ypur uploads in the ``app.instance_path/uploads``


MultiThreaded Application
-------------------------

An `UploadSet`'s configuration can be stored on the app instance itself. That way,
you can have upload sets being used by multiple apps that runs in different threads. Use the
`configure_uploads` function to store the configuration for the `UploadSet`s in
the application instance.
You pass it the app and all of the `UploadSet`s instances. Calling
`configure_uploads` more than once is safe. ::

    configure_uploads(app, (photos, media))

If your app has a factory function, that is a good place to call this
function.


File Upload Forms
-----------------

To actually upload the files, you need to properly set up your requests. As
regard ``Flask-Reuploaded`` extension, The ``uploadset.save`` method recieves
``werzeug.datastructures.FileStorage`` object as its first parameter. Any object
with other type will raise ``TypeError``.

You don't need to maually instruct this ``FileStorage`` object. Actually you
recieve it by accessing ``flask.request.files['field_name']``.

As declared by Flask_,
    
    Note that files will only contain data if the request method was POST, PUT
    or PATCH and the <form> that posted to the request had
    enctype="multipart/form-data". It will be empty otherwise. 

.. _Flask: https://flask.palletsprojects.com/en/2.1.x/api/#flask.Request.files

This means that If request method is `GET`, it won't work at all, and
if you don't set the enctype, only the filename will be transferred.

The field in the html form itself should be an ``<input type=file>``.


.. code-block:: html+jinja

    <form method=POST enctype=multipart/form-data action="{{ url_for('upload') }}">
        ...
        <input type=file name=photo>
        ...
    </form>

If you are using a client other than the browser, you should configure your
request manually to implement the flask requirements.