import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(
        sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(
        sqlalchemy.String)
    email = sqlalchemy.Column(
        sqlalchemy.String, nullable=False)
    img = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<Question> {self.title} \n {self.text} \n {self.email}'
