from flask import abort, jsonify
from flask_restful import abort, Resource

from data import db_session
from api.category_reqparser import *
from data.__all_models import *


def abort_if_categories_not_found(categories_id):
    session = db_session.create_session()
    categories = session.query(Category).get(categories_id)
    if not categories:
        abort(404, message=f"Category {categories_id} not found")


class CategoryResource(Resource):
    def get(self, categories_id):
        abort_if_categories_not_found(categories_id)
        session = db_session.create_session()
        categories = session.query(Category).get(categories_id)
        return jsonify({
            'categories': categories.to_dict(
                only=('id', 'title'))})

    def delete(self, categories_id):
        abort_if_categories_not_found(categories_id)
        session = db_session.create_session()
        category = session.query(Category).get(categories_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, categories_id):
        abort_if_categories_not_found(categories_id)
        session = db_session.create_session()
        args = parser.parse_args()
        category = session.query(Category).get(categories_id)

        if args['title']:
            category.title = args['title']

        session.commit()
        return jsonify({'success': 'OK'})


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({
            'categories': [item.to_dict(
                only=('id', 'title'))
                for item in categories]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        categories = Category()
        categories.title = args['title']

        session.add(categories)
        session.commit()
        return jsonify({'success': 'OK'})
