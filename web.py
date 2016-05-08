
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/jan/parrot/songs/'
ALLOWED_EXTENSIONS = set(['flac', 'mp3', 'm4a', '3gp', 'mp4', 'aac'])

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
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>~*~*parrot*~*~</title>
    <h1>parrot transcription suite</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file title=pick file>
         <input type=submit value=upload>
    </form>
    '''
from flask import send_from_directory

@app.route('/transcripts/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
