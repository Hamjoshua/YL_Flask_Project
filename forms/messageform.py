from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    message = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Готово')
