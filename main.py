from flask import (Flask,
    render_template,
    g,
    request,
    redirect,
    session,
    url_for,
    send_from_directory,
    flash
    )
import os
import shutil
from werkzeug.utils import secure_filename


# app = Flask()
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(32)
app.session_cookie_secure = True

# User profiling
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"

Users = []  #initialises Users list
# loading users into the list
def loadUsers():
    with open('templates/Users.txt', 'r') as Usersfiledata:
        Users.clear()
        Userfiledata = Usersfiledata.read()     #Userfiledata is the entire txt file
        Userlinedata = Userfiledata.split('\n')    #Userlinedata is each line in the txt file [namepass,namepass]
        for i in range(len(Userlinedata)-1):
            x = Userlinedata[i].split('\t')
            Users.append(User(username=x[0], password=x[1]))
    print(f"Loaded users: {Users}")
loadUsers()

@app.before_request
def before_request():
    g.user = None
    if 'user_name' in session:
        user = [x for x in Users if x.username == session['user_name']]
        if user:
            user = user[0]
            g.user = user

# routes
# home
@app.route('/')
def home():
    return render_template('home.html')

# Log in
@app.route('/login', methods=['GET','POST'])
def login():
    if g.user:
        return redirect(url_for('drive'))
    loadUsers()
    if request.method == 'POST' and request.form:
        session.pop('user_name', None)    # if 'user_name' is not found in session, pop() returns None to avoid error
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = [x for x in Users if x.username == username] # user is a Userclass object with the username that matches with entered username
        if user:    # this condition is to avoid error when no user matches with entered username
            user = user[0]
        if user and user.password == password:
            session['user_name'] = user.username
            print(f"User {user.username} *Has logged in.")
            return redirect(url_for('drive'))
        flash("Incorrect Username or Password")
    return render_template('login.html')

# create an account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and request.form:
        newusername = request.form['newusername'].strip()
        newpassword = request.form['newpassword'].strip()
        with open('templates/Users.txt', 'r') as Usersdata: # this is to get the last account number
            Userdata = Usersdata.read() # Userdata will contain the entire txt file
            Userline = Userdata.split('\n') # Userline contains each line [namepass,namepass]
        newuserdata = f"{newusername}\t{newpassword}"
        with open('templates/Users.txt', 'a') as Userswrite: #this will append new user data to the file
            Userswrite.write(newuserdata)
            Userswrite.write('\n')
            os.mkdir(f'Drive/{newusername}')
            print(f"New user {newusername} *Has been created and saved.")
            loadUsers()
            flash(f"New user {newusername} created")
            return redirect(url_for('login'))
    return render_template('signup.html')

# drive or something. wip
@app.route('/drive', methods=['GET', 'POST'])
def drive():
    if not g.user:
        return redirect(url_for('login'))
    buttonpressed = False
    if request.method == 'POST' and request.form:
        # for catching the delete account button
        buttonpressed = request.form['Delete Account']
        if buttonpressed:
            with open('templates/Users.txt', 'r') as f:
                userlines = f.read().split('\n')
                linenumber = int([x for x in range(len(userlines)-1) if userlines[x].split('\t')[0] == g.user.username][0])
                userlines.pop(linenumber)
            with open('templates/Users.txt', 'w') as Userswrite:
                userlines = '\n'.join(userlines)
                Userswrite.write(userlines)
            shutil.rmtree(f'Drive/{g.user.username}')
            session.pop('user_name', None)
            print(f"User {g.user.username} *Has been deleted.")
            flash(f"User {g.user.username} has been deleted.")
            loadUsers()
            return redirect(url_for('login'))
    if request.method == 'POST' and request.files:
        f = request.files.getlist('file')
        for i in f:
            i.save(os.path.abspath(f'Drive/{g.user.username}/{i.filename}'))
            print(f"File {i.filename} *Has been saved in Drive/{g.user.username}.")
        return redirect(url_for('drive'))

    # for fetching files
    filenames = os.listdir(f'Drive/{g.user.username}')

    # a list of extensions that are image
    imgtypes = ("apng", "avif", "bmp", "gif", "ico", "jpg", "jpeg", "jpe", "jif", "jfif", "png", "svg", "tif", "tiff", "webp", "xbm")

    return render_template('drive.html', files = filenames, imgtypes=imgtypes)

# displaying clicked file
@app.route('/drive/<path:filename>')
def displayfile(filename):
    if not g.user:
        return redirect(url_for('login'))
    print(f"File {filename} *Has been displayed.")
    return send_from_directory(
            os.path.abspath(f'Drive/{g.user.username}'),
            filename,
            as_attachment=False
            )
# downloading clicked file
@app.route('/drive/<path:filename>/download')
def downloadfile(filename):
    if not g.user:
        return redirect(url_for('login'))
    print(f"File {filename} *Has been downloaded.")
    return send_from_directory(
            os.path.abspath(f'Drive/{g.user.username}'),
            filename,
            as_attachment=True
            )

# blog
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST' and request.form:
        blogtext = request.form['blogtext'].strip()
        blogger = request.form['blogger'].strip()
        bloglist = blogger+'\t'+blogtext
        if blogtext == "":
            print("No input")
            flash('Please Enter a Message')
            return redirect(request.url)
        with open('templates/blog.txt', 'a') as blogwrite: #blog is a file
            blogwrite.write(bloglist)
            blogwrite.write('\n')
            return redirect(request.url)
    with open('templates/blog.txt', 'r') as blogdata: # blog is a file
        blog = blogdata.read()
        blogposts = blog.split('\n')
        blogposts = blogposts[::-1] # this reverses the list of blogs to put latest blog on top
        for i in range(len(blogposts)):
            blogposts[i] = blogposts[i].split('\t')
        return render_template('blog.html', posts=blogposts)

# logout page
@app.route('/logout')
def logout():
    if g.user:
        print(f"User {g.user.username} *Has logged out.")
    session.pop('user_name', None)    # if 'user_name' is not found in session, pop() returns None to avoid error
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug='True')
