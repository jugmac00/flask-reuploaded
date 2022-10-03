"""
In this example, you will be able to configure autoserving.
"""
import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

# define app
app = Flask(__name__)
# set app config
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static/img")
# set `UPLOADS_AUTOSERVE` to `True`, it is `False` by default
app.config["UPLOADS_AUTOSERVE"] = True
# create upload set
photos = UploadSet("photos", IMAGES)
# configure uploads
configure_uploads(app, photos)


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        # serve files from the `_upload.uploaded_file` endpoint
        # it takes 2 parameters, first is the setname, second is the filename
        url = url_for(
            "_uploads.uploaded_file", setname=photos.name, filename=filename
        )
        print("Url: ", url)
        return redirect(url)

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
