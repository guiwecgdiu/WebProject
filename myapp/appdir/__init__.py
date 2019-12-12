from flask import Flask
from appdir.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
moment=Moment(app)

from appdir import routes, models



