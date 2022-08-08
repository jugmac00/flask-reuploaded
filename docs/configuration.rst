Configuration
=============

UploadSet Configuration
-----------------------

You can create as many `UploadSet`s as you need. The `UploadSet` object
follows a special syntax for naming the configuration keys. The `Flask-Reuploaded`
extension will attach each `UploadSet` with its configuration according to this
syntax:

   `UPLOADED_[1]_[2]`

Where `[1]` is the capitalized set name and `[2]` is the config suffix, usually
it is one of `DEST`, `URL`, `ALLOW` or `DENY`.

As an example: If you have one set named `files`, you have the following config
keys:

- `UPLOADED_FILES_DEST`
- `UPLOADED_FILES_URL`
- `UPLOADED_FILES_ALLOW`
- `UPLOADED_FILES_DENY`


The following is the description of each configuration key.

+---------------------------+--------------------------------------------------+
|         Config Key        |                 Description                      |
+===========================+==================================================+
|   UPLOADED_FILES_DEST     | This indicates the directory that the uploaded   |
|                           | files will be saved to.                          |  
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_URL      | If you have a server set up to serve the files   |
|                           | for this set, this should be the URL they are    |
|                           | publicly accessible from. Including a trailing   |
|                           | slash.                                           |
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_ALLOW    | This config allows additional file extensions    | 
|                           | not allowed by the used upload set.              |
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_DENY     | Denies file extensions allowed by the used       | 
|                           | upload set                                       |
+---------------------------+--------------------------------------------------+


To save on configuration time, there are two settings you can provide
that apply as "defaults" if you don't provide the proper settings otherwise.


+---------------------------+--------------------------------------------------+
|         Config Key        |                 Description                      |
+===========================+==================================================+
|    UPLOADS_DEFAULT_DEST   | If an upload set's destination isn't declared,   |
|                           | then its uploads will be stored in               |
|                           | a subdirectory of this directory.                |
|                           | For example, if you set this to ``/var/uploads``,|
|                           | then a set named photos will store its uploads   |
|                           | in ``/var/uploads/photos``.                      |
+---------------------------+--------------------------------------------------+
|   UPLOADS_DEFAULT_URL     | If you have a server set up to serve from        |
|                           | `UPLOADS_DEFAULT_DEST`, then set the server's    | 
|                           | base URL here. Continuing the example above, if  |
|                           | ``/var/uploads`` is accessible from              |
|                           | ``http://localhost:5001``, then you would set    |
|                           | this to ``http://localhost:5001/`` and URLs for  |
|                           | the photos set would start with                  |
|                           | ``http://localhost:5001/photos``.                |
|                           | Include the trailing slash.                      |
+---------------------------+--------------------------------------------------+

You should ensure that each `UploadSet` you are creating has set its destination
directory, otherwise you will get a `RuntimeError` exception. To avoid this error, you
should set `UPLOADED_[SETNAME]_DEST` or `UPLOADS_DEFAULT_DEST`. 


Autoserve Configuration
-----------------------

`UPLOADS_AUTOSERVE`
Setting this configuration to `True` enables automatic viewing/downloading of uploaded files.
When the name of the `UploadSet` is `photos` and the name of the uploaded file
is `snow.jpg`, the file is available via:

    .. code-block:: python

        flask.url_for('_uploads.uploaded_file', setname='photos', filename='snow.jpg')
    

which resolves to: http://localhost:5000/_uploads/photos/snow.jpg

if you are running your server on localhost at port 5000 (The flask default)


``Default Value: In order to stay compatible with `Flask-Uploads`, for 
`Flask-Reuploaded<1.0.0` the `UPLOADS_AUTOSERVE` default is `True`. 
Since version `1.0.0` it is `False` by default.``

If you want to serve the uploaded files via http, and you expect heavy traffic,
you should think about serving the files directly via a web/proxy server, such as e.g. Nginx.


Maximum File Length Configuration
---------------------------------

By default, Flask doesn't put any limits on the size of the uploaded data. To
limit the max upload size, you can use Flask's `MAX_CONTENT_LENGTH` as
documented by Flask_ .

.. _Flask: https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/#improving-uploads

