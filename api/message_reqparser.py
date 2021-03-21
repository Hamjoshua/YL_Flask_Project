from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('message', required=True)
parser.add_argument('subtopic_id', required=True)
parser.add_argument('author_id', required=True)
