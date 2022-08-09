"""
Example application for simple usage of the `Flask-Reuploaded` extension.
In this example, You will be able to upload files, serve them.
"""
import os

from flask import Flask
from flask import abort
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

# Define app
app = Flask(__name__)
# set app config
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static/img")
# Create upload set
photos = UploadSet("photos", IMAGES)
# Configure uploads
configure_uploads(app, photos)


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        return redirect(
            url_for("show", setname=photos.name, filename=filename)
        )
    return render_template("upload.html")


@app.route("/show/<setname>/<filename>")
def show(setname, filename):
    config = current_app.upload_set_config.get(setname)  # type: ignore
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename)


if __name__ == "__main__":
    app.run()
