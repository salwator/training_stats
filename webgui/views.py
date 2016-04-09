from flask import render_template, request
from werkzeug import secure_filename
from webgui import web_gui
import os

from training_stats import half_hour_test

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
        saved_file = os.path.join(web_gui.config['USER_GPX_FOLDER'], filename)
        gpx.save(saved_file)
        lactate_thr, _, _ = half_hour_test.threshold_from_file(saved_file)
        return render_template('training.html',
                               filename=filename,
                               lactate=lactate_thr,
                               other=dir(half_hour_test))
