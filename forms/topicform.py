from csv import reader

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, \
    FileField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class TopicForm(FlaskForm):
    title = StringField('Название темы', validators=[DataRequired()])
    text = TextAreaField('Текст темы')
    img = FileField('Добавить фото', validators=[FileAllowed(['jpg', 'png'])])
    edit_img = BooleanField('Change your topic picture?', default=False)
    with open("static/categories.csv", mode='rt', encoding='utf-8') as csv_file:
        csv_file = [elem[0] for elem in reader(csv_file, delimiter=';')]
    category = SelectField(u'Категория', choices=[
        (str(num + 1), category_name) for num, category_name in enumerate(csv_file)])
    submit = SubmitField('Сохранить и применить')
