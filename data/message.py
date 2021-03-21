import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True,
                           nullable=False)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subtopic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subtopics.id'),
                                    nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')
    subtopic = orm.relation('Subtopic')
