from flask import abort, jsonify
from flask_restful import abort, Resource, reqparse, Api

from data import db_session
from api.subtopic_reqparser import *
from data.__all_models import *


def abort_if_subtopics_not_found(subtopics_id):
    session = db_session.create_session()
    subtopics = session.query(Subtopic).get(subtopics_id)
    if not subtopics:
        abort(404, message=f"subtopic {subtopics_id} not found")


class SubtopicResource(Resource):
    def get(self, subtopics_id):
        abort_if_subtopics_not_found(subtopics_id)
        session = db_session.create_session()
        subtopics = session.query(Subtopic).get(subtopics_id)
        return jsonify({
            'subtopics': subtopics.to_dict(
                only=('title', 'topic_id', 'author_id'))})

    def delete(self, subtopics_id):
        abort_if_subtopics_not_found(subtopics_id)
        session = db_session.create_session()
        subtopics = session.query(Subtopic).get(subtopics_id)
        session.delete(subtopics)
        session.commit()
        return jsonify({'success': 'OK'})


class SubtopicListResource(Resource):
    def get(self):
        session = db_session.create_session()
        subtopics = session.query(Subtopic).all()
        return jsonify({
            'subtopics': [item.to_dict(
                only=('title', 'topic_id', 'author_id'))
                for item in subtopics]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        subtopics = Subtopic()
        subtopics.title = args['title']
        subtopics.topic_id = args['topic_id']
        subtopics.author_id = args['author_id']
        session.add(subtopics)
        session.commit()
        return jsonify({'success': 'OK'})
