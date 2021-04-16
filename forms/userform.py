from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, \
    SubmitField, FileField, BooleanField
from flask_wtf.file import FileAllowed


class UserForm(FlaskForm):
    profile_img = FileField('Add profile image', validators=[FileAllowed(['jpg', 'png'])])
    edit_img = BooleanField('Change your profile picture?', default=False)
    about = TextAreaField('About')
    area = StringField('Area')
    submit = SubmitField('Save changes')
