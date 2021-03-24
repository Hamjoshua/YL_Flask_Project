from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class QuestionForm(FlaskForm):
    question_topic = StringField(
        'Question', validators=[DataRequired()])
    question_text = TextAreaField('Text')
    email = EmailField('Email', validators=[DataRequired()])
    img = FileField('Add screenshot', validators=[
        FileAllowed(['jpg', 'png'])])
    submit_question = SubmitField('Submit Question')
