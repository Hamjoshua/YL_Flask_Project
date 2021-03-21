import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Subtopic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subtopics'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True,
                           nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('topics.id'),
                                 nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)

    user = orm.relation('User')
    topic = orm.relation('Topic')

    def __repr__(self):
        return f'<Subtopic> {self.title} {self.topic_id} {self.author_id}'
