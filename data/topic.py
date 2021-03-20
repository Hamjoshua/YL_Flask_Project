from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy_serializer import SerializerMixin


class CreateTopic(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Готово')


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)

    user = orm.relation('User')

    def __repr__(self):
        return f'<Topic> {self.title} {self.author_id}'
