import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True,
        primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String)
    img = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    category_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id'), nullable=False)
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)

    user = orm.relation('User')
    category = orm.relation('Category')

    def __repr__(self):
        return f'<Subtopic> {self.title} {self.topic_id} {self.author_id}'
