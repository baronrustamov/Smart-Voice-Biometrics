import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
# from preprocessAudio import split_into_5
from subprocess import Popen, PIPE

ALLOWED_EXTENSIONS = set(['wav'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_speaker(filename):
    file_path = os.path.join(os.getcwd(), filename)

    p = Popen(["python2", "tester.py", file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    speaker_name, err = p.communicate()
    if err:
        print(err)
    speaker_name = speaker_name.decode().strip()
    return speaker_name

@app.route('/upload.html', methods=['POST'])
def register():
    return render_template('upload.html')

@app.route('/verify.html', methods=['POST'])
def verify():
    return render_template('verify.html')


@app.route('/')
def upload_form():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = str(filename).split(".")[1]
            filename = request.form['username']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + "." + file_ext))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are wav.')
            return redirect(request.url)



@app.route('/', methods=['POST'])
def verify_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = "audio.wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            speaker_name = predict_speaker(filename)
            flash("Are you {}".format(speaker_name))
            
            return render_template('verify.html', result=speaker_name)
        else:
            flash('Allowed file types are wav.')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
