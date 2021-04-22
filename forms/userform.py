from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, \
    SubmitField, FileField
from flask_wtf.file import FileAllowed


class UserForm(FlaskForm):
    profile_img = FileField(
        'Add profile image', validators=[
            FileAllowed(['jpg', 'png'])])
    about = TextAreaField('About')
    area = StringField('Area')
    submit = SubmitField('Save changes')
    delete_img = SubmitField('Удалить фото')
