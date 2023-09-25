import base64
import numpy as np
from flask import Flask, render_template, request, flash, redirect
from pkg.predict import process_img, cat_or_dog

from pprint import pprint

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "fcc0a7149b61c3c77e7de06043d8edc18dba110c7253eb06a4fc8f6aff6a985a"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img' not in request.files:
            flash("No image was uploaded", category="error")
            return redirect(request.url)
        file = request.files['img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flash("Image uploaded!", category="info")
            img = file.stream.read()
            data_b64 = base64.b64encode(img)

            data = np.asarray(bytearray(img), dtype=np.uint8)
            img = process_img(data=data)
            (confidence, result) = cat_or_dog(img)
            if result == "Dog":
                confidence = 1 - confidence
            return render_template("index.html", confidence="{:.2f}%".format(confidence*100), result=result, src=f"data:image/{file.filename.rsplit('.',1)[1]};base64, {data_b64.decode(encoding='utf-8')}")
        else:
            flash("Invalid extension!", category="error")
            return redirect(request.url)
    return render_template("index.html")
