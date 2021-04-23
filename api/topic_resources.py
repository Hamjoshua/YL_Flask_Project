from flask import abort, jsonify
from flask_restful import abort, Resource

from data import db_session
from api.topic_reqparser import *
from data.__all_models import *

from . check_api import check_api


def abort_if_topics_not_found(topics_id):
    session = db_session.create_session()
    topics = session.query(Topic).get(topics_id)
    if not topics:
        abort(404, message=f"Topic {topics_id} not found")


class TopicResource(Resource):
    @check_api
    def get(self, topics_id):
        abort_if_topics_not_found(topics_id)
        session = db_session.create_session()
        topics = session.query(Topic).get(topics_id)
        return jsonify({
            'topics': topics.to_dict(
                only=('id', 'title', 'text',
                      'img', 'date', 'category_id',
                      'author_id'))})

    @check_api
    def delete(self, topics_id):
        abort_if_topics_not_found(topics_id)
        session = db_session.create_session()
        topic = session.query(Topic).get(topics_id)
        session.delete(topic)
        session.commit()
        return jsonify({'success': 'OK'})

    @check_api
    def put(self, topics_id):
        abort_if_topics_not_found(topics_id)
        session = db_session.create_session()
        args = parser.parse_args()
        topic = session.query(Topic).get(topics_id)

        if args['title']:
            topic.title = args['title']
        if args['text']:
            topic.text = args['text']
        if args['category_id']:
            topic.author = args['category_id']
        if args['author_id']:
            topic.author = args['author_id']

        session.commit()
        return jsonify({'success': 'OK'})


class TopicListResource(Resource):
    @check_api
    def get(self):
        session = db_session.create_session()
        topics = session.query(Topic).all()
        return jsonify({
            'topics': [item.to_dict(
                only=('id', 'title', 'text',
                      'img', 'date', 'category_id',
                      'author_id'))
                for item in topics]})

    @check_api
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        topics = Topic()
        topics.title = args['title']
        topics.text = args['text']
        topics.category_id = args['category_id']
        topics.author_id = args['author_id']

        session.add(topics)
        session.commit()
        return jsonify({'success': 'OK'})
