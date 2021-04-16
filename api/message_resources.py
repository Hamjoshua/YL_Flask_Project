from flask import abort, jsonify
from flask_restful import abort, Resource

from data import db_session
from api.message_reqparser import *
from data.__all_models import *


def abort_if_message_not_found(message_id):
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Message {message_id} not found")


class MessageResource(Resource):
    def get(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        return jsonify({
            'message': message.to_dict(
                only=('message', 'topic_id',
                      'author_id', 'time'))})

    def delete(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, message_id):
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        args = parser.parse_args()
        message = session.query(Message).get(message_id)

        if args['title']:
            message.message = args['message']
        if args['topic_id']:
            message.topic_id = args['topic_id']
        if args['author_id']:
            message.author_id = args['author_id']

        session.commit()
        return jsonify({'success': 'OK'})


class MessageListResource(Resource):
    def get(self):
        session = db_session.create_session()
        message = session.query(Message).all()
        return jsonify({
            'message': [item.to_dict(
                only=('message', 'topic_id',
                      'author_id', 'time'))
                for item in message]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        message = Message()
        message.message = args['message']
        message.topic_id = args['topic_id']
        message.author_id = args['author_id']
        session.add(message)
        session.commit()
        return jsonify({'success': 'OK'})
