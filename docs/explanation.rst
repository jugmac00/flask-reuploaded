Explanation
===========


Upload Sets
-----------
``UploadSet`` is the main object provided by this extension. Each `UploadSet`
is responsible for dealing with a set of files. You had to initialize `UploadSet`:

    .. code-block:: python

        photos = UploadSet('photos', IMAGES)

And then you can use the `UploadSet.save` method to save uploaded files and
`UploadSet.path` and `UploadSet.url` to access them.

During saving and retrieving the uploaded file, the `UploadSet` object performs
some security checks for you.


Security Checks
---------------

Security itself is a huge subject and you should consider designing it
seriously. The ``Flask-Reuploaded`` extension tries to help you with preventing
some common attack vectors and user errors. for example:


- Users can't upload files with filenames that start with `.` 

e.g. `.`, '..', '../../../home/{username}/.bash' or '../../my_app.wsgi'. When
  a user tries to upload a file with such a filename, the file will be renamed.

- Users can't overwrite other users' files i.e:. `similar filenames are suffixed by a number`.
- Users can't upload files with extension suffixes that are not allowed by the ``UploadSet``.

You are advised to read the source code to explore the mechanism of dealing
with each error/attack and you may decide to take additional actions.

Another security aspect that you should consider is the maximum allowed file
size. This is ``NOT`` managed by the `Flask-Reuploaded` extension.

By default, the `Flask` application will accept file uploads of any length. It is
up to your server to save the uploaded file or fill your hard drive till
raising `No space left on device` error. You can (obviously, you should) set
the maximum allowed file length by setting the ``MAX_CONTENT_LENGTH`` configuration.
After this, `Flask` will reject files that are more than this limit.

This alone may not be enough. As uploading one thousand files of 10 MB length
might crash your server, too. This aspect is outside of the scope of this
extension but worth mentioning here.


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


Multithreaded Application
-------------------------

You can use the `configure_uploads` function to store the `UploadSet`'s
configuration in the application instance itself. That way, you can have
`UploadSet` being used by multiple applications that run in different threads. 

The `configure_uploads` function accepts two parameters. The first is the
application instance and the second is either an UploadSet instance or iterable
of UploadSet instances.
It is safe to call the `configure_uploads` function more than once. If your
application has a factory function, that is a good place to call it.

    
    .. code-block:: python


        from flask_uploads import configure_uploads

        def init_app():              
            ...            
            configure_uploads(app, (photos, media))
            ...
            return app


File Upload Forms
-----------------

To actually upload the files, you need to properly set up your requests. As
regard to the ``Flask-Reuploaded`` extension, the ``uploadset.save`` method receives
a ``werkzeug.datastructures.FileStorage`` object as its first parameter. Any object
with another type will raise ``TypeError``.

You can get `FileStorage` object by accessing the
``flask.request.files['field_name']`` where `field_type` is equal to the field
name of the uploaded file in your form.

As declared by Flask_:
    
    Note that files will only contain data if the request method was POST, PUT
    or PATCH and the <form> that posted to the request had
    enctype="multipart/form-data". It will be empty otherwise. 

.. _Flask: https://flask.palletsprojects.com/en/2.1.x/api/#flask.Request.files

This means that if the request method is `GET`, it won't work at all, and
if you don't set the enctype, only the filename will be transferred.

The field in the `HTML` form itself should be an ``<input type='file'>``.


.. code-block:: html+jinja

    <form method=POST enctype=multipart/form-data action="{{ url_for('upload') }}">
        ...
        <input type='file' name='photo'>
        <!-- Note that, your application will receive the uploaded file in -->
        <!-- `request.files['photo']`  -->
        ...
    </form>

If you are using a client other than the browser, you should configure your
request manually to implement the flask requirements.
