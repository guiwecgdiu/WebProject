from appdir import app
from flask import render_template
from datetime import datetime
from appdir.form import NameForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doc')
def doc():
    form =NameForm()
    return render_template('doc.html')


@app.errorhandler(404)
def error(error):
        return render_template('404.html'), 404

@app.errorhandler(500)
def exception(error):
        return render_template('404.html'), 500
