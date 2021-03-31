import requests

import flask
from flask import jsonify
from flask import make_response, request, Flask

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
    ll = f'{abs(upper_corner[0] - lower_corner[0])},{abs(upper_corner[1] - lower_corner[1])}'
    return toponym['Point']['pos'].replace(' ', ','), ll


@blueprint.route('/api/users_param/<string:map_type>/<int:user_id>', methods=['GET'])
def get_users_param(map_type, user_id):
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
        param['url_img'] = 'https://static.vecteezy.com/system/resources/previews/000/250/876/original/vector-error-404-unavailable-web-page-file-not-found-concept.jpg'
        return jsonify(param)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if not toponym:
        print('Not found')
        param['url_img'] = 'https://static.vecteezy.com/system/resources/previews/000/250/876/original/vector-error-404-unavailable-web-page-file-not-found-concept.jpg'
        return jsonify(param)

    ll, spn = get_ll_spn(toponym[0]["GeoObject"])
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {"ll": ll, "l": map_type, "spn": spn}
    response = requests.get(map_api_server, params=map_params)

    param['url_img'] = response.url
    print(param['url_img'])

    return jsonify(param)
