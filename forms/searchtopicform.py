from csv import reader

from flask_wtf import FlaskForm
from wtforms import StringField, \
    SubmitField, SelectField


class SearchTopicForm(FlaskForm):
    search = StringField('Поиск:')
    with open("static/categories.csv", mode='rt', encoding='utf-8') as csv_file:
        csv_file = [elem[0] for elem in reader(csv_file, delimiter=';')]
    choices = [(str(0), 'Все')] + [
        (str(num + 1), category_name)
        for num, category_name in enumerate(csv_file)]
    category = SelectField(u'Категория:', choices=choices)
    submit = SubmitField('Найти')
