from appdir import app
from flask import render_template
from datetime import datetime
from appdir.form import NameForm

@app.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@app.route('/doc')
def doc():
    form =NameForm()
    return render_template('subpage.html',form=form)


@app.errorhandler(404)
def bar(error):
        return render_template('404.html'), 404

@app.errorhandler(500)
def bar(error):
        return render_template('404.html'), 500
