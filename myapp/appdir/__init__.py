from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from appdir.config import Config

app = Flask(__name__)

moment=Moment(app)
bootstrap = Bootstrap(app) # type:Flask
app.config.from_object(Config)

if __name__ == '__main__':
    app.run()

from appdir import routes
