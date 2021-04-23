from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('role_id', required=True)
parser.add_argument('about', required=True)
parser.add_argument('area', required=True)
parser.add_argument('profile_img')
