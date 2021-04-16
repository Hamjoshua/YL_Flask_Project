import requests

import flask
from flask import Flask
from flask import jsonify, url_for

from data import db_session
from data.__all_models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


def get_ll_spn(toponym):
    lower_corner = tuple(map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))
    upper_corner = tuple(map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
    spn = f'{abs(upper_corner[0] - lower_corner[0])},{abs(upper_corner[1] - lower_corner[1])}'
    lon, lat = toponym['Point']['pos'].split()
    ll = ",".join([lon, lat])
    return ll, spn


@blueprint.route('/api/get_users_map/<string:map_type>/<int:user_id>', methods=['GET'])
def get_users_map(map_type, user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    param = dict()
    param['username'] = user.name
    param['city_from'] = user.area

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
    geocoder_params = {"apikey": api_key, "geocode": user.area, "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        param['url_img'] = url_for('static', filename='img/not_found_error.jpg')
        return jsonify(param)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if not toponym:
        print('Not found')
        param['url_img'] = url_for('static', filename='img/not_found_error.jpg')
        return jsonify(param)

    ll, spn = get_ll_spn(toponym[0]["GeoObject"])
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {"ll": ll, "l": map_type, "spn": spn}
    response = requests.get(map_api_server, params=map_params)
    param['url_img'] = response.url

    return jsonify(param)
