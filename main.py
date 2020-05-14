from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename


# app = Flask()
app = Flask(__name__, static_folder='static')

#Routes
@app.route("/")
def index():
    return render_template('index.html')

#app.config["UPLOAD_FOLDER"] = "A:/beam/uploads"
app.config["UPLOAD_FOLDER"] = "/home/websiteuser/beam/uploads"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if request.files:
            f = request.files["image"]
            if f.filename == "":
                print("No Filename")
                return redirect(request.url)
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print("File saved")
            return redirect(request.url)
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug='True')
