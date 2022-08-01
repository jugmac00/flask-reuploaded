"""
Example application for simple usage of `flask-reuploaded` extension.
In this example:
- We upload images.
- serve them manually.
- Show, How to use database storage to serve the files.
In next example, We will try the auto-serving feature.
"""
import os

from flask import Flask
from flask import abort
from flask import current_app
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

# Fake database
db = {}

# Define app
app = Flask(__name__)
# set app config
# The uploaded photo destination,
# Simply, You can use relative path like `static/img`
# But I use absolute path for this example to give the same path
# whatever the `cwd`.
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static/img")
# Create upload set
photos = UploadSet("photos", IMAGES)
# Configure uploads
configure_uploads(app, photos)
# Set routes
@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        # save info in the DB
        db.setdefault("files", []).append(
            dict(setname=photos.name, filename=filename)
        )
        # generate file urls
        url_by_filename = url_for(
            "show", setname=photos.name, filename=filename
        )
        url_by_id = url_for("show_by_id", id=len(db["files"]) - 1)
        return render_template(
            "upload.html", url_by_filename=url_by_filename, url_by_id=url_by_id
        )

        # return redirect(url_for('show', setname=photos.name, filename=filename))
    return render_template("upload.html")


@app.route("/show/<setname>/<filename>")
def show(setname, filename):
    # We know that we have only one set `photos`
    # & we can get its configs directly:. `photos.config.destination`
    # But, The following approach show how to get the configs in more complex scenario.
    config = current_app.upload_set_config.get(setname)  # type: ignore

    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename)


@app.route("/show/<int:id>")
def show_by_id(id):

    # We know that we have only one set `photos`
    # & we can get its configs directly:. `photos.config.destination`
    # But, The following approach show how to get the configs in more complex scenario.
    try:
        photo = db.get("files", [])[id]
    except IndexError:
        abort(404)
    setname = photo.get("setname")
    filename = photo.get("filename")
    config = current_app.upload_set_config.get(setname)  # type: ignore
    if config is None:
        abort(404)

    return send_from_directory(config.destination, filename)


if __name__ == "__main__":
    app.run()
