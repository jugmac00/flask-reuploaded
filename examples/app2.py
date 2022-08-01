"""
Example 2:
Example application for  usage of `flask-reuploaded` extension.
In this example:
- We upload image to specific path
- configure autoserving.
"""
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

# Define app
app = Flask(__name__)
# set app config
# The uploaded photo destination,
# Simply, In most cases, You can use relative path like `static/img`
# But I use absolute path for this example to give the same path
# whatever the `cwd`.
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static/img")
# -------------------------------------
#  Set autoserving feature           #
# -------------------------------------
app.config["UPLOADS_AUTOSERVE"] = True
# --------------------------------------------
# Create upload set
photos = UploadSet("photos", IMAGES)
# Configure uploads
configure_uploads(app, photos)

# ------------------#
# Set routes        #
# -------------------#


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        # We set UPLOADS_AUTOSERVE flag to True
        # So, We can serve files from the `_upload.uploaded_file` endpoint
        # it takes 2 parameters, first is the setname, second is the filename
        url_by_filename = url_for(
            "_uploads.uploaded_file", setname=photos.name, filename=filename
        )
        return render_template("upload.html", url_by_filename=url_by_filename)

    return render_template("upload.html")


# No need for manual serving,
# @app.route('/show/<setname>/<filename>')
# def show(setname, filename):
#     config = current_app.upload_set_config.get(setname)  # type: ignore
#     if config is None:
#         abort(404)
#     return send_from_directory(config.destination, filename)


if __name__ == "__main__":
    app.run()
