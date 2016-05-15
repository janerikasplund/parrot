"""This code allows a user to upload a
file to the server and then have it
processed into a Google Cloud API-friendly
FLAC file"""

import glob, time, os, subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

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
        # for each file uploaded with the allowed extension
        if file and allowed_file(file.filename):
            # secures the file according to werkzeug method
            filename = secure_filename(file.filename)
            # splits filename into stringname and extension
            stringname, file_extension = os.path.splitext(filename)
            # saves the uploaded file to "UPLOAD_FOLDER" defined above
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # iterates over every file in the "songs" directory that was just uploaded 
            for file.filename in sorted(glob.glob("/home/jan/parrot/songs/%s" % filename)):
                # create a new directory with the filename title
                subprocess.call('mkdir /home/jan/parrot/songs/%s' % stringname, shell=True)
                # converts uploaded file into a series of 16-bit, mono flac files, each totaling 50 seconds or less
                subprocess.call('sox /home/jan/parrot/songs/%s --channels=1 --bits=16 /home/jan/parrot/songs/%s/%s.flac \
				-q trim 0 50 : newfile : restart' % (filename, stringname, stringname), shell=True)
                # change the working directory to the directory we created
                os.chdir("/home/jan/parrot/songs/%s" % stringname)
                # iterates over every file in the working directory with the wildcard name sox creates
                for file in sorted(glob.glob(stringname + "0*.flac")):
                # now we run each file in the working directory through speech_rest.py
                    subprocess.call('python /home/jan/parrot/speech_rest.py /home/jan/parrot/songs/%s/%s \
				    >>/home/jan/parrot/songs/%s/%s-transcript.txt' % (stringname, file, stringname, \
				    stringname), shell=True)
                    global count
                    count += 1
                # wait a little bit thanks to Google's usage limits!
                    time.sleep(5)
                    print  "Working on file " + str(count) + "..."
                    for file in sorted(glob.glob("/home/jan/parrot/songs/%s/%s-transcript.txt" % (stringname, stringname))):
                # move the transcript to flask's static directory, from which it can be served
                        subprocess.call('mv /home/jan/parrot/songs/%s/%s-transcript.txt /home/jan/parrot/static/%s-transcript.txt' \
					% (stringname, stringname, stringname), shell=True)
                        transcription = '%s-transcript.txt' % stringname
                        return redirect(url_for('transcribed_file', transcription=transcription))

@app.route('/<transcription>')
def transcribed_file(transcription):
    return send_from_directory(app.config['TRANSCRIPT_FOLDER'],
                              transcription)

#            return render_template('hello2.html', my_string="%s" % stringname)

if __name__ == '__main__':
    app.run(debug=True)
