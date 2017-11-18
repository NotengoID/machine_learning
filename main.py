#from flask import Flask, render_template, request
#app = Flask(__name__)

#@app.route('/')
#def form():
#    return render_template('form.html')

#@app.route('/submitted', methods=['POST'])
#def submitted_form():
#    name = request.form['name']
#    email = request.form['email']
#    site = request.form['site_url']
#    comments = request.form['comments']
#    return render_template(
#    'submitted_form.html',
#    name=name,
#    email=email,
#    site=site,
#    comments=comments)

import os
#import numpy as np
import ocrdni
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST','GET'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        height = '1' #str(cv2.IMREAD_UNCHANGED)
        width = 'wi' + ocrdni.leerImagenDeRequest(file)
        #height, width = file.shape[:2]
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('submitted_form.html',
            name=filename,
            height=height,
            width=width)
