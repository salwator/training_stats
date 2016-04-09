from webgui import web_gui

@web_gui.route('/')
def index():
    return 'Hello world!'

