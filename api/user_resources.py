from flask import abort, jsonify
from flask_restful import abort, Resource, reqparse, Api

from data import db_session
from api.user_reqparser import *
from data.__all_models import *


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"users {users_id} not found")


class UserResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({
            'users': users.to_dict(
                only=('name', 'hashed_password', 'role_id'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(
                only=('name', 'hashed_password', 'role_id'))
                for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User()
        users.name = args['name']
        users.set_password(args['password'])
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
