from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
