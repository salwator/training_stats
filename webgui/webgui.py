from flask import Flask

web_gui = Flask(__name__)
web_gui.config['USER_GPX_FOLDER'] = 'webgui/uploaded_gpx/'
