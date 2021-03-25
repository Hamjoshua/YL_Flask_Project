from csv import reader

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileStorage


class UserForm(FlaskForm):
    profile_img = FileField('Add profile image', validators=[FileAllowed(['jpg', 'png'])])
    edit_img = BooleanField('Change your profile picture?', default=False)
    about = TextAreaField('About')
    area = StringField('Area')
    submit = SubmitField('Save changes')
