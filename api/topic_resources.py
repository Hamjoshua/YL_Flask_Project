from flask import abort, jsonify
from flask_restful import abort, Resource, reqparse, Api

from data import db_session
from api.topic_reqparser import *
from data.__all_models import *


def abort_if_topics_not_found(topics_id):
    session = db_session.create_session()
    topics = session.query(Topic).get(topics_id)
    if not topics:
        abort(404, message=f"topic {topics_id} not found")


class TopicResource(Resource):
    def get(self, topics_id):
        abort_if_topics_not_found(topics_id)
        session = db_session.create_session()
        topics = session.query(Topic).get(topics_id)
        return jsonify({
            'topics': topics.to_dict(
                only=('title', 'author_id'))})

    def delete(self, topics_id):
        abort_if_topics_not_found(topics_id)
        session = db_session.create_session()
        topics = session.query(Topic).get(topics_id)
        session.delete(topics)
        session.commit()
        return jsonify({'success': 'OK'})


class TopicListResource(Resource):
    def get(self):
        session = db_session.create_session()
        topics = session.query(Topic).all()
        return jsonify({
            'topics': [item.to_dict(
                only=('title', 'author_id'))
                for item in topics]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        topics = Topic()
        topics.title = args['title']
        topics.author_id = args['author_id']
        session.add(topics)
        session.commit()
        return jsonify({'success': 'OK'})
