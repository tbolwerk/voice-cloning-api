import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/twan/iquality/Voice-Clone-Project/Real-Time-Voice-Cloning-master/Real-Time-Voice-Cloning-master/uploads'
ALLOWED_EXTENSIONS = {'wav','mp3','m4a'}
DEFAULT_OUTPUT_AUDIO_FILENAME = "demo_output_00.wav"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        sentence = request.form['sentence']
        if(sentence is None):
            return "Sentence must me between 20+- characters"
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_audio_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_audio_file)

            if filename.endswith(".mp3"):
                old_uploaded_audio_file = uploaded_audio_file
                converted_audio_file = filename.split('.')
                new_converted_audio_file = f"{converted_audio_file[0]}.wav" 
                uploaded_audio_file = os.path.join(app.config['UPLOAD_FOLDER'], new_converted_audio_file)                                               
                os.system(f"ffmpeg -i {old_uploaded_audio_file} -acodec pcm_u8 {uploaded_audio_file}")
            if filename.endswith(".m4a"):
                old_uploaded_audio_file = uploaded_audio_file
                converted_audio_file = filename.split('.')
                new_converted_audio_file = f"{converted_audio_file[0]}.wav" 
                uploaded_audio_file = os.path.join(app.config['UPLOAD_FOLDER'], new_converted_audio_file)                                               
                os.system(f"ffmpeg -i {old_uploaded_audio_file} -acodec pcm_s16le -ac 2 {uploaded_audio_file}")                 

            cmd = f"python3 api_client.py -a '{sentence}' -f {uploaded_audio_file}"

            os.system(cmd)
            return redirect(url_for('uploaded_file',
                                    filename=DEFAULT_OUTPUT_AUDIO_FILENAME))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>      
      <label for=sentence>Text input:</label>
      <input type=text name=sentence id=sentence value=What do you want me to say!>
      <input type=submit value=Upload>
    </form>   '''