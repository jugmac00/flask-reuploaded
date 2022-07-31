Getting Started
===============

The following code snippets explain how to quickly integrate the extension in your application.

1. First you need to configure at least one ``UploadSet``:

    .. code-block:: python

        # IMAGES is a collection of the most common image suffixes.
        from flask_uploads import IMAGES
        from flask_uploads import UploadSet
        # Create your first `UploadSet`.
        photos = UploadSet("photos", IMAGES)

2. You should set the required configurations:

    .. code-block:: python

        # Choose a destination where the image uploads will be saved to.
        app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
        # Store the uploadset in the app instance, so we can use it later
        configure_uploads(app, photos)

3. Use `photos` UploadSet set to save files in your view function:   
    
    .. code-block:: python

        @app.route('/', methods=['GET', 'POST'])
        def upload():
           ...
           # Assign the filename to a variable, as you will need it when you want to serve the files.
           filename = photos.save(request.files['photo'])
        
4. Serve your files (manually):

    .. code-block:: python

        @app.route('/show/<setname>/<filename>')
        def show(setname, filename):
            config = current_app.upload_set_config.get(setname)  # type: ignore
            if config is None:
                abort(404)
            return send_from_directory(config.destination, filename)
