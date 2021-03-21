from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SubtopicForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Готово')
