from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)
parser.add_argument('category_id', required=True)
parser.add_argument('author_id', required=True)
