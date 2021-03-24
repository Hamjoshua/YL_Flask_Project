import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'roles'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    role = sqlalchemy.Column(
        sqlalchemy.String, unique=True, nullable=False)
