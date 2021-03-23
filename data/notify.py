import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Notify(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'notify'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True,
                           nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                nullable=False)
    href = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user = orm.relation('User')

    def __repr__(self):
        return f'<Notify> {self.text} {self.href}'
