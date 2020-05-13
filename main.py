from flask import Flask, render_template, request, redirect
import os


# app = Flask()
app = Flask(__name__, static_folder='static')

#Routes
@app.route("/")
def index():
    return render_template('index.html')

app.config["UPLOAD_FOLDER"] = "A:/beam/uploads"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.files:
            f = request.files['image']
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
            return redirect(request.url)
            print('File has been successfully uploaded')
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)