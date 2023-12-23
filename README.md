<div>
<img align=right width=60% src=Picture1.jpg \>

## Overview

### beam components
* Username-Password authentication
* Cookies to rememeber logged-in user
* Personal drive for each user to save their files in
* Preview for photos and images for convenience
* Bonus blog page for learning file handling
</div>
<div align=center>
    <img align=center width=90% src=Picture2.jpg>
</div>

---

## How to run
* Recommended to use [Git Bash](https://gitforwindows.org/)
* Clone repository to your computer using SSH:  
`git clone git@github.com:vihankarnik/beam.git`
* Create and activate virtual environment using python module `virtualenv` in beam home directory:  
`pip3 install virtualenv`  
`python3 -m virtualenv venv`  
`source venv/bin/activate`
* Install all required dependencies listed in `requirements.txt` into the virtual environment `venv`  
`pip3 install -r requirements.txt`
* Run program using the deployment file `wsgi.py`  
`python3 wsgi.py`
* By default the server runs on port `5000` on the IP address `127.0.0.1`
* If you run this script as a user with normal privileges (recommended), you might not have access to start a port on a low port number. Low port numbers are reserved for the superuser (root).
* Access the website on `http://127.0.0.1:5000`

#### Modules used:
* The User-Interface is written in HTML and CSS.
* The backend of this application which is purely written in `Python` is powered by a micro web framework called `Flask` which utilises a templating engine called `Jinja2` to display the webpage templates. Handling of files is done through Python module `os`.
* The client sends the uploaded file using a `POST` request and this is received by the server backend which is written in Python and securely saved. Downloading files is done through `GET` requests.
