from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

MAP_TYPES = [('map', 'map'), ('sat', 'sat'), ('skl', 'skl')]


class MapForm(FlaskForm):
    map_type = SelectField('Тип карты:', choices=MAP_TYPES, default=MAP_TYPES[0][0])
    submit = SubmitField('Применить')
