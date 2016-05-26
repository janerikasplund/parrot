"""This code allows a user to upload a
file to the server and then have it
processed into a Google Cloud API-friendly
FLAC file"""

import glob, time, os, subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pdb

UPLOAD_FOLDER = '/home/jan/parrot/songs/'
ALLOWED_EXTENSIONS = set(['flac', 'mp3', 'wav'])
TRANSCRIPT_FOLDER = '/home/jan/parrot/static/'
count = 0

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPT_FOLDER'] = TRANSCRIPT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stringname, file_extension = os.path.splitext(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            for file.filename in sorted(glob.glob("/home/jan/parrot/songs/%s" % filename)):
                subprocess.call('mkdir /home/jan/parrot/songs/%s' % stringname, shell=True)
                subprocess.call('sox /home/jan/parrot/songs/%s --channels=1 --bits=16 /home/jan/parrot/songs/%s/%s.flac \
				-q trim 0 50 : newfile : restart' % (filename, stringname, stringname), shell=True)
                os.chdir("/home/jan/parrot/songs/%s" % stringname)
                global count
                onlyfiles = next(os.walk("/home/jan/parrot/songs/%s" % stringname))[2]
                tally = len(onlyfiles)
		# need to fix the bug where the last line ends up on top as the first line, maybe by tinkering with the count fuinction
                while count < tally:
                    for file in sorted(glob.glob(stringname + "0*.flac")):
                        subprocess.call('python /home/jan/parrot/speech_rest.py /home/jan/parrot/songs/%s/%s \
				    >>/home/jan/parrot/static/%s-transcript.txt &' % (stringname, file, stringname), shell=True)
                        count += 1
                        time.sleep(5)
                        print  "Working on file " + str(count) + "..."
                time.sleep(50)
                print "Waiting..."
#                transname = ('%s-transcript.txt' % stringname)
#                return redirect(url_for('transcribed_file', transname=transname)) 
                transcription = '/home/jan/parrot/static/%s-transcript.txt' % stringname
		transopen = open(transcription)
		transtext = transopen.read()
		return render_template('hello2.html', my_string="%s" % transtext)

# @app.route('/uploads/<transname>/')
# def transcribed_file(transname):
#     return send_from_directory(app.config['TRANSCRIPT_FOLDER'],
#					  transname)

if __name__ == '__main__':
    app.run(debug=True)
