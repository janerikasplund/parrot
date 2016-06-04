"""This code allows a user to upload a
file to the server and then have it
processed into a Google Cloud API-friendly
FLAC file"""

import glob, time, os, subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pdb
import shutil

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

	    # standard werkzeug method for making sure a file isn't malicious

            filename = secure_filename(file.filename)
            stringname, file_extension = os.path.splitext(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	    ''' We make a new directory here and run the Sox command
		that will give us several equally long audio files
		from the original.  '''
	
            for file.filename in sorted(glob.glob("/home/jan/parrot/songs/%s" % filename)):
                subprocess.call('mkdir /home/jan/parrot/songs/%s' % stringname, shell=True)
                subprocess.call('sox /home/jan/parrot/songs/%s --channels=1 --bits=16 /home/jan/parrot/songs/%s/%s.flac \
				-q trim 0 20 : newfile : restart' % (filename, stringname, stringname), shell=True)
                os.chdir("/home/jan/parrot/songs/%s" % stringname)
                global count

		''' Find all the files created by Sox
                    in the /songs/ directory and count them.
		    Only counts files matching the 
	 	    stringname from the uploaded file. '''

                onlyfiles = next(os.walk("/home/jan/parrot/songs/%s" % stringname))[2]
                tally = len(onlyfiles)

		''' Call speech_rest.py on each file,
		    output the results to a .txt file,
                    and do so only as long as the number
                    of operations is below the overall 
                    number of files created. '''

                while count < tally:
                    for file in sorted(glob.glob(stringname + "0*.flac")):
                        subprocess.call('python /home/jan/parrot/speech_rest.py /home/jan/parrot/songs/%s/%s \
				    >>/home/jan/parrot/static/%s-transcript.txt &' % (stringname, file, stringname), shell=True)
                        count += 1
                        time.sleep(5)
                        print  "Working on file " + str(count) + "..."
                time.sleep(15)
                print "Waiting..."

		''' The Google Cloud Speech API has strict usage limits
		    so the above Waiting and Sleeping is necessary for now. '''

                transcription = '/home/jan/parrot/static/%s-transcript.txt' % stringname

		# Using os.remove() and shutil.rmtree() to clean up those big audio files after we're done

		os.remove("/home/jan/parrot/songs/%s" % filename)
		shutil.rmtree("/home/jan/parrot/songs/%s" % stringname)
		transopen = open(transcription)
		transtext = transopen.read()
		return render_template('hello2.html', my_string="%s" % transtext)

if __name__ == '__main__':
    app.run(debug=True)
