import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Topic> {self.title} {self.author_id}'
