from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename


# app = Flask()
app = Flask(__name__, static_folder='static')

# routes
# home
@app.route('/')
def home():
    return render_template('home.html')

# about
@app.route('/about')
def about():
    return render_template('about.html')

# blog
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST' and request.form:
        blogtext = request.form['blogtext']
        blogger = request.form['blogger']
        bloglist = blogger+'\t'+blogtext
        if blogtext == "":
            print("No input")
            return redirect(request.url)
        with open('uploads/posts.txt', 'a') as blogwrite:
            blogwrite.write(bloglist)
            blogwrite.write('\n')
            return redirect(request.url)
    with open('uploads/posts.txt', 'r') as blogdata:
        blog = blogdata.read()
        blogposts = blog.split('\n')
        for i in range(len(blogposts)):
            blogposts[i] = blogposts[i].split('\t')
        return render_template('blog.html', posts=blogposts)

# upload
app.config['UPLOAD_FOLDER'] = "uploads/"
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST" and request.files:
        f = request.files["file"]
        if f.filename == "":
            print("No Filename")
            return redirect(request.url)
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print("File saved")
        return redirect(request.url)
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug='True')