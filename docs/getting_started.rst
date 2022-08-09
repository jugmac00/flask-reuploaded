Getting Started
===============

The following code snippets explain how to quickly integrate the extension in your application.

1. First You need to configure at least one ``UploadSet``

    .. code-block:: python

        # IMAGES is a list containing all image suffixes.
        from flask_uploads import IMAGES
        from flask_uploads import UploadSet
        # Create your first `UploadSet`.
        photos = UploadSet("photos", IMAGES)

2. You should set the required configurations:

    .. code-block:: python

        # Configure your Flask app destination for the `photos` `Uploadset`.
        app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
        # Store the uploadset in the app instance, So we can use it later
        configure_uploads(app, photos)

3. Use `photos` UploadSet set to save files in your view function:   
    
    .. code-block:: python

        @app.route('/', methods=['GET', 'POST'])
        def upload():
           ...
           # save the filename, You will need it when you want to serve the files.
           filename = photos.save(request.files['photo'])
        
4. Serve your files (manually):

    .. code-block:: python

        @app.route('/show/<setname>/<filename>')
        def show(setname, filename):
            config = current_app.upload_set_config.get(setname)  # type: ignore
            if config is None:
                abort(404)
            return send_from_directory(config.destination, filename)

.. 
    TODO: In order to keep this file small & easy, this step will be moved to the 
          explanation file. 

.. 5. Optionally, You can use the extension to autoserve your files:

..     .. code-block:: python
        
..         # Step 1: same as mentioned in `Step 1` above.
..         # Step 2:
..         app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
..         # Note: For autoserving, you should set `UPLOADS_AUTOSERVE` to `True` 
..         # before calling `configure_uploads`
..         app.config["UPLOADS_AUTOSERVE"] = True
..         # Store the uploadset in the app instance, So we can use it later
..         configure_uploads(app, photos)
..         # Step 3: same as mentioned in `Step 3` above.
..         # Step 4: Serve you files from this url
..         url = url_for('_uploads.uploaded_file', setname=photos.name, filename=filename)
..         # If you have `photos` UploadSet and you uploaded `snow.jpeg` 
..         # the above url will resolve to:
..         # url = "127.0.0.1:5000/photos/snow.jpeg" assuming that you serve your 
..         # application on "127.0.0.1:5000"

