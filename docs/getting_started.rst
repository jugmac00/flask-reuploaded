Getting started
===============

The following code snippets explains how to quickly integrate the extension in your application.

1. First You need to configure UploadSet/s

    .. code-block:: python

        # IMAGES is a list containing all images suffixes
        from flask_uploads import IMAGES, configure_uploads, UploadSet
        # Create your first `UploadSet`
        photos = UploadSet("photos", IMAGES)

2. You should set the required configurations:

    .. code-block:: python

        # Configure your Flask app
        # destination for the `photos` uploadset.
        app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
        # Store the uploadset in the app instance, So we can use it later
        configure_uploads(app, photos)

3. Use `photos` UploadSet set to save files in your view function:   
    
    .. code-block:: python

        @app.route('/', methods=['GET', 'POST'])
        def upload():
           ...
           # get the filename, You may need it when you want to serve the files
           filename = photos.save(request.files['photo'])
        
4. Serve your files (manually):

    .. code-block:: python

        @app.route('/show/<setname>/<filename>')
        def show(setname, filename):
            config = current_app.upload_set_config.get(setname)  # type: ignore
            if config is None:
                abort(404)
            return send_from_directory(config.destination, filename)

5. Optionally, You can use the extension to autoserve your files.

    .. code-block:: python
        
        # Don't forget to set `UPLOADS_AUTOSERVE` to True
        app.config["UPLOADS_AUTOSERVE"] = True
        
        # Your files are located here
        url_for('_uploads.uploaded_file', setname=photos.name, filename=filename)
        # uploadset : is the `UploadSet` instance you have created in step:. 1
        # In our example, the `photos.name` equals 'photos'
        # File name is the value returned from 
        # `photos.save(request.files['photo'])`
        # You got in step:. 3
        