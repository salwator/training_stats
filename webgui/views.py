from flask import render_template, request
from werkzeug import secure_filename
from webgui import web_gui
import os


@web_gui.route('/')
def index():
    ''' Render landing page '''
    return render_template('index.html',
                           title='Home')


@web_gui.route('/upload', methods=['POST'])
def upload():
    ''' Serve upload file request '''
    gpx = request.files['file']
    
    def is_gpx(filename):
        return filename.rsplit('.', 1)[1].lower() == 'gpx'
    
    if gpx and is_gpx(gpx.filename):
        filename = secure_filename(gpx.filename)
        gpx.save(os.path.join(web_gui.config['USER_GPX_FOLDER'], filename))
        return render_template('training.html',
                               filename=filename)
