import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topics'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)

    user = orm.relation('User')

    def __repr__(self):
        return f'<Topic> {self.title} {self.author_id}'
