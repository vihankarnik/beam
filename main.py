from flask import Flask, render_template, request


# app = Flask()
app = Flask(__name__, static_folder='static')

#Routes
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('uploaded_file.txt')


if __name__ == "__main__":
    app.run(debug=True)