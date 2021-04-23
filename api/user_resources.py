from flask import abort, jsonify
from flask_restful import abort, Resource

from data import db_session
from api.user_reqparser import *
from data.__all_models import *

from . check_api import check_api


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UserResource(Resource):
    @check_api
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({
            'users': users.to_dict(
                only=('id', 'name', 'email', 'role_id', 'about', 'area',
                      'profile_img', 'apikey'))})

    @check_api
    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        args = parser.parse_args()
        user = session.query(User).get(users_id)

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.set_password(args['password'])
        if args['role_id']:
            user.title = args['role_id']
        if args['about']:
            user.title = args['about']
        if args['area']:
            user.title = args['area']

        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(
                only=('id', 'name', 'email', 'role_id', 'about', 'area',
                      'profile_img', 'apikey'))
                for item in users]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        users = User()
        users.name = args['name']
        users.set_password(args['password'])
        users.email = args['email']
        users.role_id = args['role_id']
        users.area = args['area']
        users.about = args['about']

        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
