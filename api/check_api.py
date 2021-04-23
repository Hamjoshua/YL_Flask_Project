from flask import request
from flask_restful import abort

from data import db_session
from data.__all_models import *


def check_api(function):
    def inner(*args, **kwargs):
        try:
            apikey = request.headers['apikey']
            db_sess = db_session.create_session()
            if not db_sess.query(User).filter(User.apikey == apikey).first():
                raise Exception
        except Exception:
            abort(403, message='Invalid API-key')
        return function(*args, **kwargs)
    return inner