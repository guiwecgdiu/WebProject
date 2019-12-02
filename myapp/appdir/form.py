from flask_wtf import Form
from wtforms import StringField, SubmitField,PasswordField,DateField
from wtforms.validators import Required
from flask_wtf.file import FileField,FileRequired,FileAllowed


class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    cv=FileField('Your CV',validators=[FileRequired(),FileAllowed(['jpg','png','gif'])])
    submit = SubmitField('Submit')

class DateForm(Form):
    """docstring for ."""
    username=StringField("Username",validators=[Required()])
    password=PasswordField("Password",validators=[Required()])
    submit=SubmitField('Submit')

class UploadForm(Form):
    """docstring for ."""
    cv=FileField('Your CV',validators=[FileRequired(),FileAllowed(['jpg','png','gif'])])
    submit=SubmitField('Submit')
