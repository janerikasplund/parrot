"""This code allows a user to upload a
file to the server and then have it
processed into a Google Cloud API-friendly
FLAC file"""

import glob, time
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import subprocess
import sys

UPLOAD_FOLDER = '/home/jan/parrot/songs/'
ALLOWED_EXTENSIONS = set(['flac', '.vimrc', '.bashrc'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            for file.filename in sorted(glob.glob("/home/jan/parrot/songs/*.flac")):
                subprocess.call('sox /home/jan/parrot/songs/%s --channels=1 --bits=16 /home/jan/parrot/songs/%s -q trim 0 50 : newfile : restart' % (filename, filename), shell=True)
                return render_template('hello2.html')
    return render_template('hello.html')




# from flask import send_from_directory

#@app.route('/transcripts/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'],
#                               filename)

if __name__ == '__main__':
    app.run(debug=True)
