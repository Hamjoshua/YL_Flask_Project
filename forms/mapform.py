from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

MAP_TYPES = ['map', 'sat', 'skl']


class MapForm(FlaskForm):
    map_type = SelectField('Тип карты:', choices=MAP_TYPES, default=MAP_TYPES[1])
    submit = SubmitField('Применить')
