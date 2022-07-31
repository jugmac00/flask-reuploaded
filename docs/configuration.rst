Configuration
=============

UploadSet configuration:
------------------------

The `UploadSet` has special syntax of configuration, which is `UUPLOADED_(1)_(2)`
The `(1)` is the capitalized set name & the `(2)` is the config suffix, usually
it is `DEST`, `URL`, `ALLOW` or `DENY`.

As An example: If you have one set named `files`, You have the following configs
- `UPLOADED_FILES_DEST`
- `UPLOADED_FILES_URL`
- `UPLOADED_FILES_ALLOW`
- `UPLOADED_FILES_DENY`

The following is the description of each configuration item.

+---------------------------+--------------------------------------------------+
|         Config Key        |                 Description                      |
+===========================+==================================================+
|   UPLOADED_FILES_DEST     | This indicates the directory uploaded files will |
|                           |         will be saved to.                        |  
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_URL      | If you have a server set up to serve the files   |
|                           | in this set, this should be the URL they are     |
|                           | publicly accessible from. Include the trailing   |
|                           | slash files will be saved to.                    |
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_ALLOW    | This lets you allow file extensions not allowed  |
|                           | by the upload set in the Code.                   |
+---------------------------+--------------------------------------------------+
|   UPLOADED_FILES_DENY     | This lets you deny file extensions allowed by    | 
|                           | the upload set in the code.                      |
+---------------------------+--------------------------------------------------+


You should ensure that you had set destination for each `UploadSet` you are
creating. To save on configuration time, there are two settings you can provide
that apply as "defaults" if you don't provide the proper settings otherwise.


+---------------------------+--------------------------------------------------+
|         Config Key        |                 Description                      |
+===========================+==================================================+
|    UPLOADS_DEFAULT_DEST   | if an upload set's destination isn't declared,   |
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

Autoserve configuration:
------------------------

`UPLOADS_AUTOSERVE`
    Setting this configuration to `True` enables automatic viewing/downloading of uploaded files.
    Default: In order to stay compatible with `Flask-Uploads`,  for `Flask-Reuploaded` < 1.0.0 
    `UPLOADS_AUTOSERVE` defaulted to `True`.
    Since version `1.0.0` `UPLOADS_AUTOSERVE` defaults to `False`,


    When the name of the `UploadSet` is `photos` and the name of the uploaded
    file is `snow.jpg`, the file is available via
    `flask.url_for('_uploads.uploaded_file', setname='photos', filename='snow.jpg')` which
    resolve to: `http://localhost:5000/_uploads/photos/snow.jpg`.

    
If you want to serve the uploaded files via http, and you expect heavy traffic,
you should think about serving the files directly by a web/proxy server as e.g. Nginx.



By default Flask doesn't put any limits on the size of the uploaded
data. To limit the max upload size, you can use Flask's `MAX_CONTENT_LENGTH`.