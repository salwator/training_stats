from flask import render_template
from webgui import web_gui

@web_gui.route('/')
def index():
    return render_template('index.html',
                           title='Home')

