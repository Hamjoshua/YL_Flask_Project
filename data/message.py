from .db_session import SqlAlchemyBase

import datetime
import sqlalchemy

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class MessageForm(FlaskForm):
    message = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subtopic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subtopics.id'),
                                   nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')
    subtopic = orm.relation('Subtopic')
